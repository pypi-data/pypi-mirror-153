/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { withStyles } from '@mui/styles';
import { Button, Dialog, DialogContent, DialogTitle, IconButton } from '@mui/material';
import { Close } from '@mui/icons-material';
import { ShadowedDivider } from '../../core';
import { FileMetadata } from '../deploy/fileBrowser/FileBrowser';
import { FilterableFile } from '../deploy/fileBrowser/DirListingContent';
import DirListingItem from '../deploy/fileBrowser/DirListingItem';

interface IProps {
	metadata: FileMetadata
    onDownload?: (file: FileMetadata) => void
    onDelete?: (file: FileMetadata) => void
    onClose?: () => any
}

// Properties for this component
interface IState {
    open: boolean
    organizedFiles: FileMetadata[]
}

const StyledDialog = withStyles({
    root: {
        margin: '12px',
        padding: '0px',
    },
    paper: {
        backgroundColor: 'var(--jp-layout-color1)',
        width: 'calc(min(80%, 600px + 2px))',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog)

export class VersionHistory extends React.Component<IProps, IState> {
	_isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            open: false,
            organizedFiles: this.organizeFiles(), 
        }
    }

    private organizeFiles = () => {
        const newChildren: FileMetadata[] = []
        // Combine multiple children that are the same file
        for (let child of this.props.metadata.content) {
            var match = false
            for (let newChild of newChildren) {
                if (newChild.hash == child.hash) {
                    newChild.content.push(child)
                    match = true
                    break
                }
            }
            if (!match) {
                const newChild: FileMetadata = JSON.parse(JSON.stringify(child))
                newChild.content = [JSON.parse(JSON.stringify(newChild))]
                newChildren.push(newChild)
            }
        }
        return newChildren
    }

	public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
            <>
                <StyledDialog
                    open={this.state.open}
                    onClose={() => {
                        if (this.props.onClose) this.props.onClose()
                        this.safeSetState({ open: false })
                    }}
                >
                    <DialogTitle sx={{
                        display: 'inline-flex',
                        height: '60px',
                        padding: '6px',
                    }}>
                        <DIV sx={{
                            display: 'inline-flex',
                            width: '100%',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <DIV sx={{margin: 'auto 12px'}}>
                                Version history
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1}} />
                        <IconButton
                            size='large'
                            onClick={() => this.safeSetState({ open: false })}
                            sx={{
                                display: 'inline-block',
                                width: '36px',
                                height: '36px',
                                padding: '3px',
                                margin: '6px',
                            }}
                        >
                            <Close
                                sx={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
					</DialogTitle>
                    <ShadowedDivider />
                    <DIV>
                        <DialogContent sx={{padding: '8px', lineHeight: '24px', fontSize: 'var(--jp-ui-font-size0)'}}>
                            {this.state.organizedFiles.map(metadata => (
                                <DirListingItem 
                                    file={{ file: metadata, indices: [] } as FilterableFile }
                                    filter={null}
                                    selected={false}
                                    showReferences={true}
                                    showVersionHistory={false}
                                    onClick={() => void 0}
                                    onDoubleClick={() => void 0}
                                    onDownload={this.props.onDownload}
                                    onDelete={this.props.onDelete == undefined ? undefined : 
                                        (file: FileMetadata) => {
                                            // Remove the file from the internal state
                                            const sortedFiles = this.state.organizedFiles.filter(x => x.path != file.path || x.hash != file.hash)
                                            this.setState({ organizedFiles: sortedFiles, open: sortedFiles.length > 0 })
                                            // Perform the passed in action
                                            this.props.onDelete(file)
                                        }
                                    }
                                />
                            ))}
                        </DialogContent>
                    </DIV>
                </StyledDialog>
                <Button 
                    onClick={() => this.safeSetState({ open: true })}
                >
                    Version history
                </Button>
            </>
		);
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		this._isMounted = false;
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

	// public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
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
