/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SPAN } from '../Global';

import { TreeView, TreeItem } from '@mui/lab'
import { withStyles } from '@mui/styles';
import { ChevronRight, ExpandMore } from '@mui/icons-material';

import FileExtensionIcon from './FileExtensionIcon';
import { FileMetadata } from './deploy/fileBrowser/FileBrowser';
import moment from 'moment';
import FormatUtils from '../utils/FormatUtils';
import { Button } from '@mui/material';
import FileServerUtils from '../utils/FileServerUtils';

type TreeNode = DirectoryNode | FileNode

export interface DirectoryNode {
    path: string
    file: string
    children: TreeNode[]
    metadata: undefined
}

export interface FileNode {
    path: string
    file: string
    metadata: FileMetadata[]
    children: undefined
}

interface IProps {
    files: FileMetadata[]
    fileHidableIcon?: (file: FileNode) => JSX.Element
    directoryHidableIcon?: (directory: DirectoryNode) => JSX.Element
}

interface IState {
    expanded: string[]
}

const fileTitle = (file: FileNode) => (
    'Name: ' + file.metadata[0].name + '\n' +
    (file.metadata[0].size === null ? '' : 'Size: ' + FormatUtils.styleCapacityUnitValue()(file.metadata[0].size) + (Global.isDevVersion ? ' (' + file.metadata[0].size + ' bytes)' : '') + '\n') +
    (file.metadata[0].path === '' ? '' : 'Path: ' + file.metadata[0].path.replace(file.metadata[0].name, '').replace(/\/$/, '') + '\n') + 
    'Modified: ' + file.metadata.map(x => moment(x.last_modified).format('YYYY-MM-DD hh:mm:ss')).join(', ')
)

export class FileTree extends React.Component<IProps, IState> {

    public static childrenToMetadata = (directory: DirectoryNode, includeDuplicateHashes: boolean = true): FileMetadata[] => {
        const metadata: FileMetadata[] = []
        for (let child of directory.children) {
            if (child.children) {
                metadata.push(...FileTree.childrenToMetadata(child as DirectoryNode, includeDuplicateHashes))
            } else {
                if (includeDuplicateHashes) {
                    metadata.push(...(child as FileNode).metadata)
                } else {
                    metadata.push((child as FileNode).metadata[0])
                }
            }
        }
        return metadata
    }

    constructor(props: IProps) {
        super(props);
        
        this.state = {
            expanded: [],
        }
    }

    private renderTreeItems = (files: FileMetadata[]): JSX.Element[] | undefined => {

        const generateTreeStructure = (): TreeNode => {

            const generatePathStructure = (metadata: FileMetadata, path: string, file: string): TreeNode => {
                var startedWithSquiggleSlash = false
                if (file.startsWith('~/')) {
                    file = file.replace('~/', '')
                    startedWithSquiggleSlash = true
                }
                let parts = file.split(/(?<=^\/?[^\/]+)(?=\/)/)
                if (parts.length > 1) {
                    return {
                        path: path,
                        file: (startedWithSquiggleSlash ? '~/' : '') + parts[0],
                        children: [generatePathStructure(metadata, (startedWithSquiggleSlash ? '~/' : '') + path + parts[0], parts[1])]
                    } as DirectoryNode
                } else {
                    return { path: path, file: (startedWithSquiggleSlash ? '~/' : '') + file, metadata: [metadata] } as FileNode
                }
            }

            const mergePathStructure = (treeStructure: TreeNode, pathStructure: TreeNode): TreeNode => {
                if (treeStructure.children === undefined) {
                    treeStructure.children = [pathStructure]
                    return treeStructure
                } else if (pathStructure.children === undefined) {
                    treeStructure.children.push(pathStructure)
                    return treeStructure
                } else {
                    for (let i = 0; i < treeStructure.children.length; i++) {
                        let child = treeStructure.children[i]
                        if (child.file === pathStructure.file) {
                            treeStructure.children[i] = mergePathStructure(child, pathStructure.children[0])
                            return treeStructure
                        }
                    }
                    treeStructure.children.push(pathStructure)
                    return treeStructure
                }
            }

            let treeStructure: TreeNode = {path: '', file: '', children: []} as DirectoryNode
            for (let file of files) {
                let pathStructure = generatePathStructure(file, '', file.path)
                treeStructure = mergePathStructure(treeStructure, pathStructure)
            }
            return treeStructure
        }

        const collapseTreeStructure = (structure: TreeNode): TreeNode => {
            if (structure.children === undefined) {
                return structure                
            } else if (structure.children.length === 1) {
                let child = structure.children[0]
                structure.file += child.file
                structure.metadata = child.metadata
                structure.children = child.children
                return collapseTreeStructure(structure)
            } else {
                for (let i = 0; i < structure.children.length; i++) {
                    structure.children[i] = collapseTreeStructure(structure.children[i])
                }
                return structure
            }
        }

        const combineTreeStructure = (structure: TreeNode): TreeNode => {
            const newChildren: TreeNode[] = []
            // Combine multiple children that are the same file
            if (structure.children) {
                for (let child of structure.children) {
                    var match = false
                    for (let newChild of newChildren) {
                        if (child.metadata && newChild.metadata && newChild.metadata[0].path == child.metadata[0].path) {
                            (newChild as FileNode).metadata.push(child.metadata[0])
                            match = true
                            break
                        }
                    }
                    if (!match) newChildren.push(child)
                }

                for (let child of newChildren) {
                    if (child.metadata) child.metadata.sort(FileServerUtils.sortFiles)
                }

                // Update the children in the structure
                structure.children = newChildren
                // Call this recursively for children
                for (let i = 0; i < structure.children.length; i++) {
                    structure.children[i] = combineTreeStructure(structure.children[i])
                }
            }
            return structure
        }

        const renderTreeStructure = (structure: TreeNode, includeSlash: boolean): JSX.Element => {
            let hasChildren = structure.children && structure.children.length > 1
            return (
                <FileTreeItem
                    structure={structure}
                    includeSlash={includeSlash}
                    includeReferences={false}
                    title={hasChildren ? (
                        ''
                    ) : (
                        fileTitle(structure as FileNode)
                    )}
                    hidableIcon={hasChildren ? (
                        this.props.directoryHidableIcon ? this.props.directoryHidableIcon(structure as DirectoryNode) : undefined
                    ) : (
                        this.props.fileHidableIcon ? this.props.fileHidableIcon(structure as FileNode) : undefined
                    )}
                >
                    {hasChildren ? structure.children.map((child: TreeNode) => renderTreeStructure(child, false)) : ([] as JSX.Element[])}
                </FileTreeItem>
            )
        }

        let structure: TreeNode = combineTreeStructure(generateTreeStructure())

        return Array.isArray(structure.children) ? (
            structure.children.map((child: TreeNode) => renderTreeStructure(collapseTreeStructure(child), true))
        ) : undefined
    }

    private i = 0;

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');

        const key = (this.i++).toString()

        return (
            <TreeView
                key={key}
                disableSelection
                defaultCollapseIcon={<ExpandMore />}
                defaultExpandIcon={<ChevronRight />}
                expanded={this.state.expanded}
                onNodeToggle={(event: React.ChangeEvent<{}>, nodeIds: string[]) => {
                    this.setState({ expanded: nodeIds })
                }}
            >
                {this.renderTreeItems(this.props.files)}
            </TreeView>
        )
    }

    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

interface ItemProps {
    structure: TreeNode
    includeSlash: boolean
    includeReferences: boolean
    title?: string
    hidableIcon: JSX.Element
    children?: JSX.Element[]
}

interface ItemState {
    hovered: boolean
    visibleChildren: JSX.Element[]
    currentPage: number
}

const INITIAL_SIZE = 10
const PAGE_SIZE = 100

class FileTreeItem extends React.Component<ItemProps, ItemState> {
    private _isMounted = false
    private StyledTreeItem: any

    constructor(props: ItemProps) {
        super(props)

        this.StyledTreeItem = withStyles({
            root: {
                width: '100%',
            },
            label: {
                display: 'flex',
                width: 'calc(100% - 19px)',
                alignItems: 'center',
            }
        })(TreeItem)

        this.state = {
            hovered: false,
            visibleChildren: this.props.children.slice(0, INITIAL_SIZE),
            currentPage: 0,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const structure = this.props.structure
        const nodeId = structure.path + " " + structure.file + " " + structure.metadata?.length + " " + (structure.metadata && structure.metadata.length > 0 ? structure.metadata[0].hash : '')
        return (
            <DIV
                key={nodeId}
                sx={{display: 'flex', width: '100%', position: 'relative'}}
            >
                <this.StyledTreeItem
                    nodeId={nodeId}
                    endIcon={<FileExtensionIcon path={structure.file}/>}
                    label={(
                        <DIV
                            onMouseOver={() => this.safeSetState({hovered: true})}
                            onMouseOut={() => this.safeSetState({hovered: false})}
                            title={this.props.title}
                            sx={{
                                height: '34px',
                                lineHeight: '34px',
                                flexGrow: 1,
                                fontSize: 'var(--jp-ui-font-size1)',
                                fontFamily: 'var(--jp-ui-font-family)',
                                overflowX: 'hidden',
                                whiteSpace: 'nowrap',
                                textOverflow: 'ellipsis',
                            }}
                        >
                            {structure.file.replace(this.props.includeSlash ? '' : /^\//, '') /*+ (hasChildren ? '/' : '')*/}
                            {this.props.includeReferences && structure.metadata && structure.metadata.length > 1 && (
                                <SPAN sx={{marginLeft: '6px', opacity: '0.5'}}>
                                    {'is referenced by ' + structure.metadata.length + ' workloads'}
                                </SPAN>
                            )}
                        </DIV>
                    )}
                >   
                    {this.state.visibleChildren.length == 0 ? undefined : (
                        <>
                            {this.state.visibleChildren}
                            {this.props.children.length > INITIAL_SIZE && ((this.state.currentPage * PAGE_SIZE) + INITIAL_SIZE < this.props.children.length) && (
                                <Button
                                    sx={{flexGrow: 1}}
                                    onClick={() => {
                                        const newPage = this.state.currentPage + 1
                                        this.setState({ currentPage: newPage, visibleChildren: this.props.children.slice(0, (newPage * PAGE_SIZE) + INITIAL_SIZE) })
                                    }}
                                >
                                    Show more
                                </Button>
                            )}
                        </>
                    )}
                </this.StyledTreeItem>
                {this.props.hidableIcon && (
                    <DIV 
                        sx={{
                            display: 'inline-flex', 
                            position: 'absolute', 
                            right: '0px', 
                            opacity: this.state.hovered ? 1 : 0, 
                            transition: 'opacity 300ms ease-in-out'
                        }}
                        onMouseOver={() => this.safeSetState({hovered: true})}
                        onMouseOut={() => this.safeSetState({hovered: false})}
                    >
                        {this.props.hidableIcon}
                    </DIV>
                )}
                {structure.metadata && (
                    <DIV sx={{
                        display: 'inline-flex', 
                        position: 'absolute', 
                        right: '12px', 
                        opacity: this.state.hovered ? 0 : 0.5, 
                        transition: 'opacity 300ms ease-in-out',
                        lineHeight: '36px',
                        fontSize: 'var(--jp-ui-font-size1)',
                        pointerEvents: 'none'
                    }}>
                        {moment(structure.metadata[0].last_modified).fromNow()}
                    </DIV>
                )}
            </DIV>
        );
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

    // public shouldComponentUpdate = (nextProps: ItemProps, nextState: ItemState): boolean => {
    //     try {
    //         if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
    //         if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
    //         if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
    //         return false;
    //     } catch (error) {
    //         return true;
    //     }
    // }
}
