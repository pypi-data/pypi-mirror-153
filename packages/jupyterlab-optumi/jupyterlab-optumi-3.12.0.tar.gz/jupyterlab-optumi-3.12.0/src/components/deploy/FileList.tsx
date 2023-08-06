/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { IconButton } from '@mui/material';
import { GetApp } from '@mui/icons-material';

import { FileMetadata } from './fileBrowser/FileBrowser';
import { DirectoryNode, FileNode, FileTree } from '../FileTree';
import { App } from '../../models/application/App';
import FileServerUtils from '../../utils/FileServerUtils';
import { Status } from '../../models/Module';

interface IProps {
	app: App;
}

// Properties for this component
interface IState {
	overwrite: boolean
}

export class FileList extends React.Component<IProps, IState> {
	_isMounted = false;

	constructor(props: IProps) {
		super(props);
		this.state = {
			overwrite: false
		};
	}

	private getFileHidableIcon = (file: FileNode) => {
		return (
			<>
				{this.props.app.getAppStatus() != Status.COMPLETED || Global.user.fileTracker.pathExists(file.path + file.file) ? (
					<IconButton
						size='large'
						onClick={() => this.downloadFiles([file.metadata[0]])}
						sx={{ width: '36px', height: '36px', padding: '4px 3px 2px 3px' }}
					>
						<GetApp sx={{ width: '30px', height: '30px', padding: '3px' }} />
					</IconButton>
				) : (
					<DIV sx={{lineHeight: '34px', opacity: '0.5', margin: 'auto 6px'}}>
						File removed
					</DIV>
				)}
			</>
			
		)
	}

	private getDirectoryHidableIcon = (directory: DirectoryNode) => {
		// TODO:JJ Disable this if the entire directory has been disabled
		return (
			<>
				{this.props.app.getAppStatus() != Status.COMPLETED || Global.user.fileTracker.directoryExists(directory.path + directory.file) ? (
					<IconButton
						size='large'
						onClick={() => this.downloadFiles(FileTree.childrenToMetadata(directory, false), directory.path)}
						sx={{ width: '36px', height: '36px', padding: '4px 3px 2px 3px' }}
					>
						<GetApp sx={{ width: '30px', height: '30px', padding: '3px' }} />
					</IconButton>
				) : (
					<DIV sx={{lineHeight: '34px', opacity: '0.5', margin: 'auto 6px'}}>
						Directory removed
					</DIV>
				)}
			</>
		)
	}

	private getFiles() {
		const inputFiles: FileMetadata[] = [];
		const outputFiles: FileMetadata[] = [];
		for (let module of this.props.app.modules) {
            if (module.files) {
                for (let file of module.files) {
                    outputFiles.push(file);
                }
            }
		}
		for (let file of this.props.app.files) {
			inputFiles.push(file);
		}
		var sortedInput: FileMetadata[] = inputFiles.sort(FileServerUtils.sortFiles);
		var sortedOutput: FileMetadata[] = outputFiles.sort(FileServerUtils.sortFiles);
		return (
            <DIV>
				<DIV>
					<DIV sx={{fontWeight: 'bold'}}>
						Input files
					</DIV>
					{sortedInput.length == 0 ? (
						<DIV>
							No input files
						</DIV>
					) : (
						<FileTree
							files={sortedInput}
							fileHidableIcon={this.getFileHidableIcon}
							directoryHidableIcon={this.getDirectoryHidableIcon}
						/>
					)}
				</DIV>
				<DIV>
					<DIV sx={{fontWeight: 'bold', marginTop: '16px'}}>
						Output files
					</DIV>
					{sortedOutput.length == 0 ? (
						<DIV>
							No output files
						</DIV>
					) : (
						<FileTree
							files={sortedOutput}
							fileHidableIcon={this.getFileHidableIcon}
							directoryHidableIcon={this.getDirectoryHidableIcon}
						/>
					)}
				</DIV>
			</DIV>
        );
	}

	private downloadFiles = (files: FileMetadata[], directory: string = null) => {
		const withHashes = [];
		const withoutHashes = [];
        for (let file of files) {
			if (file.hash) {
				withHashes.push(file);
			} else {
				withoutHashes.push(file);
			}
        }
		if (withHashes.length > 0) Global.user.fileTracker.downloadFiles(withHashes[0].path, withHashes, false, directory);
		if (withoutHashes.length > 0) Global.user.fileTracker.getNotebookOutputFiles(withoutHashes[0].path, withoutHashes, this.props.app.uuid, this.props.app.modules[0].uuid, false, directory);
	}

	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
			<DIV sx={{padding: '12px', width: "100%"}}>
				{this.getFiles()}
			</DIV>
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

	// private safeSetState = (map: any) => {
	// 	if (this._isMounted) {
	// 		let update = false
	// 		try {
	// 			for (const key of Object.keys(map)) {
	// 				if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
	// 					update = true
	// 					break
	// 				}
	// 			}
	// 		} catch (error) {
	// 			update = true
	// 		}
	// 		if (update) {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
	// 			this.setState(map)
	// 		} else {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
	// 		}
	// 	}
	// }

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
