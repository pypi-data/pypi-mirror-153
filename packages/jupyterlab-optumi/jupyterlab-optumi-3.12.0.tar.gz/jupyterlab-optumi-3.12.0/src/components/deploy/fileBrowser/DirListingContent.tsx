/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global, UL } from '../../../Global';

import { StringExt } from '@lumino/algorithm';

import DirListingItem from './DirListingItem'
import { FileMetadata } from './FileBrowser'
import Button from '@mui/material/Button';

export class FilterableFile {
    file: FileMetadata;
    indices: number[];

    constructor(file: FileMetadata) {
        this.file = file;
        this.indices = [];
    }
} 

interface IProps {
    filter: string
    files: FileMetadata[]
    onOpen: (file: FileMetadata) => void
    sort: (a: FileMetadata, b: FileMetadata) => number
    getSelected: (getSelected: () => FileMetadata[]) => void
    onDownload?: (file: FileMetadata) => void
    onDelete?: (file: FileMetadata) => void
}

interface IState {
    selected: FileMetadata[]
    filteredSortedFiles: FilterableFile[]
    visibleFiles: FilterableFile[]
    currentPage: number
}

const PAGE_SIZE = 100

export default class DirListingContent extends React.Component<IProps, IState> {
    private _isMounted = false

    firstClicked: FileMetadata // Pressing enter operates on this file
    lastClicked: FileMetadata

    constructor(props: IProps) {
        super(props)
        if (this.props.getSelected) this.props.getSelected(() => this.state.selected)
        const filteredSortedFiles = this.props.files.map(x => new FilterableFile(x)).filter(this.filter).sort((a, b) => this.props.sort(a.file, b.file))
        this.state = {
            selected: [],
            filteredSortedFiles: filteredSortedFiles,
            visibleFiles: filteredSortedFiles.slice(0, PAGE_SIZE),
            currentPage: 0,
        }
    }

    private filter = (filterableFile: FilterableFile): boolean => {
        // Jupyterlab does not filter on directories, but we do
        // if (filterableFile.file.type === 'directory') return true;
        // Run the fuzzy search for the item and query.
        const name = filterableFile.file.name.toLowerCase();
        const query = this.props.filter.toLowerCase();
        let score = fuzzySearch(name, query);
        // Ignore the item if it is not a match.
        if (!score) {
            filterableFile.indices = [];
            return false;
        }
        filterableFile.indices = score.indices;
        return true;
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <UL className='jp-DirListing-content' sx={{overflowY: 'auto'}}>
                {this.state.visibleFiles.map(filteredFile => (
                    <DirListingItem
                        key={filteredFile.file.path + filteredFile.file.name}
                        file={filteredFile}
                        filter={this.props.filter}
                        selected={this.state.selected.includes(filteredFile.file)}
                        showReferences={false}
                        showVersionHistory={true}
                        onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                            // If we are not interested in selecting, do nothing on a single click
                            if (this.props.getSelected) {
                                if (this.firstClicked === undefined) {
                                    if (event.shiftKey) {
                                        this.firstClicked = this.state.filteredSortedFiles[0].file
                                        this.lastClicked = this.state.filteredSortedFiles[0].file
                                    } else {
                                        this.firstClicked = filteredFile.file
                                    }
                                }
                                if (event.ctrlKey) {
                                    const newSelected = [...this.state.selected]
                                    if (newSelected.includes(filteredFile.file)) {
                                        newSelected.splice(newSelected.indexOf(filteredFile.file), 1)
                                    } else {
                                        newSelected.push(filteredFile.file)
                                    }
                                    this.safeSetState({selected: newSelected})
                                    this.lastClicked = filteredFile.file
                                } else if (event.shiftKey) {
                                    const newSelected = [...this.state.selected]
                                    let index = this.state.filteredSortedFiles.indexOf(filteredFile)
                                    const lastClickedIndex = this.state.filteredSortedFiles.map(x => x.file).indexOf(this.lastClicked)
                                    const direction = index < lastClickedIndex ? 1 : -1
                                    while (!newSelected.includes(this.state.filteredSortedFiles[index].file) && index !== lastClickedIndex) {
                                        newSelected.push(this.state.filteredSortedFiles[index].file)
                                        index += direction
                                    }
                                    if (index === lastClickedIndex && !newSelected.includes(this.lastClicked)) newSelected.push(this.lastClicked);
                                    this.safeSetState({selected: newSelected})
                                } else {
                                    this.safeSetState({selected: [filteredFile.file]})
                                    this.firstClicked = filteredFile.file
                                    this.lastClicked = filteredFile.file
                                }
                            }
                        }}
                        onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                            if (!event.ctrlKey && !event.shiftKey) {
                                this.safeSetState({selected: []})
                                this.props.onOpen(filteredFile.file)
                            }
                        }}
                        onDownload={this.props.onDownload}
                        onDelete={this.props.onDelete == undefined ? undefined : 
                            (file: FileMetadata) => {
                                // Remove the file from the internal state
                                for (let x of this.state.filteredSortedFiles) {
                                    // We only want to remove the entry if there are no references left
                                    if (x.file.path == file.path && x.file.content && file.content && x.file.content.length == file.content.length) {
                                        const filteredSortedFiles = this.state.filteredSortedFiles.filter(x => x.file.path != file.path) 
                                        this.setState({ filteredSortedFiles: filteredSortedFiles, visibleFiles: filteredSortedFiles.slice(0, (this.state.currentPage + 1) * PAGE_SIZE) })
                                    }
                                }
                                // Perform the passed in action
                                this.props.onDelete(file)
                            }
                        }
                    />
                ))}
                {this.state.filteredSortedFiles.length > PAGE_SIZE && (((this.state.currentPage + 1) * PAGE_SIZE) < this.state.filteredSortedFiles.length) && (
                    <Button
                        sx={{width: '100%'}}
                        onClick={() => {
                            const newPage = this.state.currentPage + 1
                            this.setState({ currentPage: newPage, visibleFiles: this.state.filteredSortedFiles.slice(0, (newPage + 1) * PAGE_SIZE) })
                        }}
                    >
                        Show more
                    </Button>
                )}
            </UL>
        )
    }

    public componentDidUpdate = (prevProps: IProps, prevState: IState) => {
        if (JSON.stringify(prevProps) !== JSON.stringify(this.props)) {
            const filteredSortedFiles = this.props.files.map(x => new FilterableFile(x)).filter(this.filter).sort((a, b) => this.props.sort(a.file, b.file))
            this.safeSetState({ filteredSortedFiles: filteredSortedFiles, visibleFiles: filteredSortedFiles.slice(0, (this.state.currentPage + 1) * PAGE_SIZE) });
        }
    } 

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}
}

/// The functions below were taken from https://github.com/jupyterlab/jupyterlab/blob/879385b7cb9eba2a5d5975035b481f0c69022782/packages/filebrowser/src/search.tsx

/**
 * A text match score with associated content item.
 */
 interface IScore {
    /**
     * The numerical score for the text match.
     */
    score: number;

    /**
     * The indices of the text matches.
     */
    indices: number[] | null;
}

/**
 * Perform a fuzzy search on a single item.
 */

function fuzzySearch(source: string, query: string): IScore | null {
    // Set up the match score and indices array.
    let score = Infinity;
    let indices: number[] | null = null;
  
    // The regex for search word boundaries
    const rgx = /\b\w/g;
  
    let continueSearch = true;
  
    // Search the source by word boundary.
    while (continueSearch) {
      // Find the next word boundary in the source.
      let rgxMatch = rgx.exec(source);
  
      // Break if there is no more source context.
      if (!rgxMatch) {
        break;
      }
  
      // Run the string match on the relevant substring.
      let match = StringExt.matchSumOfDeltas(source, query, rgxMatch.index);
  
      // Break if there is no match.
      if (!match) {
        break;
      }
  
      // Update the match if the score is better.
      if (match && match.score <= score) {
        score = match.score;
        indices = match.indices;
      }
    }
  
    // Bail if there was no match.
    if (!indices || score === Infinity) {
      return null;
    }
  
    // Handle a split match.
    return {
      score,
      indices
    };
  }
