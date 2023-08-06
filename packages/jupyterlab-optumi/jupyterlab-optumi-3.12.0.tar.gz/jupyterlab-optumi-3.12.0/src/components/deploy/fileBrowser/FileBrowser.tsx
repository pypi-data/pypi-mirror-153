/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../../Global';

import { SxProps, Theme } from '@mui/system';

import { PageConfig } from '@jupyterlab/coreutils';

import { ISignal } from '@lumino/signaling';

import BreadCrumbs from './BreadCrumbs';
import DirListing from './DirListing';
import FilterBox from './FilterBox';

export interface FileMetadata {
    content: Array<FileMetadata> | null,
    created: string,
    format: string | null,
    last_modified: string,
    mimetype: string | null,
    name: string,
    path: string,
    size: number | null,
    type: 'notebook' | 'file' | 'directory',
    writable: boolean,
    hash: string,
}

interface IProps {
    sx?: SxProps<Theme>
    request: (path: string) => Promise<any>
    getSelectedFiles?: (getSelectedFiles: () => FileMetadata[]) => void
    onAdd?: () => void
    onDownload?: (file: FileMetadata) => void
    onDelete?: (file: FileMetadata) => void
    updateSignal?: ISignal<any, void>
}

interface IState {
    serverRoot: string,
    root: FileMetadata,
    path: FileMetadata[],
    files: FileMetadata[],
    filter: string,
}

export default class FileBrowser extends React.Component<IProps, IState> {
    private _isMounted = false
    private oldOpen: (event: MouseEvent) => boolean

    private getSelected: () => FileMetadata[]

    constructor(props: IProps) {
        super(props)
        if (this.props.getSelectedFiles) this.props.getSelectedFiles(this.getSelectedFiles)
        this.state = {
            serverRoot: PageConfig.getOption('serverRoot'),
            root: undefined,
            path: [],
            files: [],
            filter: '',
        }
    }

    private getSelectedFiles = (): FileMetadata[] => {
        // We don't want to return the internal contents in case they are changed
        return JSON.parse(JSON.stringify(this.getSelected())) as FileMetadata[];
    }

    private handleOpen = (file: FileMetadata) => {
        if (file.type === 'directory') {
            this.props.request(file.path).then(json => {
                const newPath = [...this.state.path]
                const depth = file.path.replace(/[^/]/g, '').length
                while (newPath.length > depth) newPath.pop();
                if (file !== this.state.root) newPath.push(file)
                this.safeSetState({
                    path: newPath,
                    files: [...json.content],
                })
            })
        } else {
            if (this.props.onAdd) this.props.onAdd();
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV className='jp-FileBrowser' sx={this.props.sx}>
                <FilterBox onChange={(filter: string) => this.safeSetState({filter})} />
                <BreadCrumbs serverRoot={this.state.serverRoot} root={this.state.root} path={this.state.path} onOpen={this.handleOpen} />
                <DirListing
                    filter={this.state.filter}
                    files={this.state.files}
                    onOpen={this.handleOpen}
                    getSelected={this.props.getSelectedFiles ? getSelected => this.getSelected = getSelected : undefined}
                    onDownload={this.props.onDownload}
                    onDelete={this.props.onDelete}
                />
            </DIV>
        )
    }

    private handleUpdate = () => {
        this.props.request(this.state.path.length == 0 ? '' : this.state.path[this.state.path.length-1].path).then(json => {
            this.safeSetState({files: json.content});
        })
    }

    public componentDidMount = () => {
        this._isMounted = true
        this.props.request('').then(json => {
            this.safeSetState({root: json, files: json.content});
        })
        // Override the JupyterLab context menu open (disable it)
        this.oldOpen = Global.lab.contextMenu.open;
        Global.lab.contextMenu.open = () => false;
        if (this.props.updateSignal) this.props.updateSignal.connect(this.handleUpdate)
    }

    // Add context menu items back
    public componentWillUnmount = () => {
        // Restore the old JupyterLab context menu open
        Global.lab.contextMenu.open = this.oldOpen;
        this._isMounted = false
        if (this.props.updateSignal) this.props.updateSignal.disconnect(this.handleUpdate)
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