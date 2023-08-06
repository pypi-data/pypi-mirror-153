/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SkinnyButton } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

import { SxProps, Theme } from '@mui/system';
import { Button, Dialog, DialogTitle, IconButton } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Close } from '@mui/icons-material';

import { ShadowedDivider } from '../../core';
import FileBrowser, { FileMetadata } from './fileBrowser/FileBrowser';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        // width: '100%',
        height: '80%',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog);

interface IProps {
    sx?: SxProps<Theme>
    onOpen?: () => void
    onClose?: () => void
    onFilesAdded: (paths: FileMetadata[]) => void
}

interface IState {
    open: boolean,
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class AddFilesPopup extends React.Component<IProps, IState> {
    private _isMounted = false

    private getSelectedFiles: () => FileMetadata[] = () => []

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
		};
    }
    
    private handleClickOpen = () => {
        if (this.props.onOpen) this.props.onOpen()
		this.safeSetState({ open: true });
	}

	private handleClose = () => {
        this.safeSetState({ open: false });
        if (this.props.onClose) this.props.onClose()
    }
    
    private handleAdd = () => {
        const files = this.getSelectedFiles()
        if (files.length > 0) {
            this.props.onFilesAdded(files)
            this.handleClose()
        }
    }

    private handleKeyDown = (event: KeyboardEvent) => {
        // The enter has to be a timeout because without it the file gets added but the popup doesn't close
        if (event.key === 'Enter') setTimeout(() => this.handleAdd(), 0);
        if (event.key === 'Escape') this.handleClose();
    }

    private request = async (path: string) => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'api/contents/' + path;
		return ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json();
		})
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({display: 'inline-flex', width: '50%'}, this.props.sx)} >
                <SkinnyButton
                    onClick={this.handleClickOpen}
                    disableElevation
                    color={"primary"} 
                    variant={"contained"}
                    fullWidth
                    sx={{ margin: '6px'}}
                >
                    + Upload
                </SkinnyButton>
                <StyledDialog
					open={this.state.open}
					onClose={this.handleClose}
                    scroll='paper'
				>
					<DialogTitle sx={{
                        display: 'inline-flex',
                        height: '60px',
                        padding: '6px',
                    }}>
                        <DIV sx={{
                            display: 'inline-flex',
                            minWidth: '225px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <DIV sx={{margin: 'auto', paddingLeft: '12px'}}>
            					Select files or directories
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1}} />
                        <DIV>
                            <Button
                                disableElevation
                                sx={{ height: '36px', margin: '6px' }}
                                variant='contained'
                                color='primary'
                                onClick={this.handleAdd}
                            >
                                Add
                            </Button>
                        </DIV>
                        <IconButton
                            size='large'
                            onClick={this.handleClose}
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
                    <FileBrowser sx={{maxHeight: 'calc(100% - 60px - 2px)'}} request={this.request} onAdd={this.handleAdd} getSelectedFiles={(getSelectedFiles: () => FileMetadata[]) => this.getSelectedFiles = getSelectedFiles} />
				</StyledDialog>
            </DIV>
        );
    }

    public componentDidMount = () => {
        this._isMounted = true
        Global.setLink(Global.Target.DeployTab.FilesAccordion.UploadPopup, () => this.safeSetState({open: true}))
        document.addEventListener('keydown', this.handleKeyDown, false)
    }

    public componentWillUnmount = () => {
        document.removeEventListener('keydown', this.handleKeyDown, false)
        Global.deleteLink(Global.Target.DeployTab.FilesAccordion.UploadPopup)
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
