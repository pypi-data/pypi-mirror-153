/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { Checkbox, CircularProgress, IconButton } from '@mui/material';
import { CheckBoxOutlineBlank as CheckBoxOutlineBlankIcon, CheckBox as CheckBoxIcon, Close as CloseIcon, Cached as CachedIcon } from '@mui/icons-material';

import { FileUploadConfig } from "../../models/FileUploadConfig";
import ExtraInfo from '../../utils/ExtraInfo';
import FormatUtils from '../../utils/FormatUtils';
import DirListingItemIcon from './fileBrowser/DirListingItemIcon';

interface RFProps {
    file: FileUploadConfig,
    handleFileEnabledChange: (enabled: boolean) => void,
    handleFileDelete: () => void,
    missingLocally: boolean,
    missingInCloud: boolean,
}

interface RFState {
    hovering: boolean,
    fileSync: boolean,
}

export class ResourceFile extends React.Component<RFProps, RFState> {
    _isMounted: boolean = false

    constructor(props: RFProps) {
        super(props)
        this.state = {
            hovering: false,
            fileSync: this.props.file.enabled,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const progress = Global.user.fileTracker.get(this.props.file.path);
        const compression = progress.filter(x => x.type == 'compression');
        const upload = progress.filter(x => x.type == 'upload');

        // Decide what color to make this
        // Green is if the file exists on the disk and can be synced
        // Yellow is if it doesn't exist on the disk but exists in the cloud so we can still run
        // Red is if it doesn't exist locally or in the cloud so we can't run
        // Always show is set based on color (green/gray false, red/orange true)
        var syncColor;
        var alwaysShowFileSync;
        if (this.state.fileSync) {
            if (!this.props.missingLocally) {
                syncColor = 'success';
                alwaysShowFileSync = false;
            } else {
                if (!this.props.missingInCloud) {
                    syncColor = 'warning';
                    alwaysShowFileSync = true;
                } else {
                    syncColor = 'error';
                    alwaysShowFileSync = true;
                }
            }
        } else {
            syncColor = 'text.disabled';
            alwaysShowFileSync = false;
        }

        return (
            <DIV
                sx={{display: 'flex', width: '100%', position: 'relative'}}
                onMouseOver={() => {
                    this.safeSetState({hovering: true})
                }}
                onMouseOut={() => {
                    this.safeSetState({hovering: false})
                }}
            >
                <DIV sx={{
                    position: 'absolute',
                    left: '-10px',
                    paddingTop: '3px', // The checkbox is 16px, the line is 22px
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: Global.easeAnimation,
                }}>
                    <Checkbox
                        disableRipple
                        checked={this.state.fileSync}
                        sx={{padding: '0px'}}
                        icon={<CheckBoxOutlineBlankIcon sx={{width: '16px', height: '16px'}} />}
                        checkedIcon={<CheckBoxIcon sx={{width: '16px', height: '16px'}} />}
                        onClick={() => {
                            let newFileSync = !this.state.fileSync
                            this.safeSetState({fileSync: newFileSync})
                            this.props.handleFileEnabledChange(newFileSync);
                        }}
                    />
                </DIV>
                <DIV sx={{
                    position: 'absolute',
                    right: '-10px',
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: Global.easeAnimation,
                }}>
                    <IconButton
                        size='large'
                        onClick={this.props.handleFileDelete}
                        sx={{
                            width: '22px',
                            height: '22px',
                            padding: '0px',
                            position: 'relative',
                            display: 'inline-block',
                        }}
                    >
                        <CloseIcon sx={{position: 'relative', width: '16px', height: '16px'}} />
                    </IconButton>
                </DIV>
                <DIV sx={{
                    position: 'absolute',
                    right: '9px',
                    paddingTop: '3px', // The checkbox is 16px, the line is 22px
                    display: 'inline-flex',
                    transition: Global.easeAnimation,
                }}>
                    {!this.props.missingLocally && (compression.length > 0 && compression[0].total >= 0) ? (
                        <ExtraInfo reminder={compression.length > 0 ? compression[0].total == -1 ? '' : 'Compressed ' + compression[0].progress + '/' + compression[0].total + ' files' : ''}>
                            <DIV sx={{height: '16px', width: '16px', background: 'var(--jp-layout-color1)'}}>
                                <CircularProgress
                                    color='primary'
                                    size='14px'
                                    thickness={8}
                                    sx={{margin: 'auto'}}
                                />
                            </DIV>
                        </ExtraInfo>
                    ) : (!this.props.missingLocally && (upload.length > 0 && upload[0].total >= 0) ? (
                        <ExtraInfo reminder={FormatUtils.styleCapacityUnitValue()(upload[0].progress) + '/' + FormatUtils.styleCapacityUnitValue()(upload[0].total)}>
                            <DIV sx={{height: '16px', width: '16px', background: 'var(--jp-layout-color1)'}}>
                                <CircularProgress
                                    variant='determinate'
                                    size='14px'
                                    thickness={8}
                                    sx={{margin: 'auto'}}
                                    value={(upload[0].progress / upload[0].total) * 100 }
                                />
                            </DIV>
                        </ExtraInfo>
                    ) : (
                        <CachedIcon sx={{
                            position: 'relative',
                            width: '16px',
                            height: '16px',
                            transform: 'scaleX(-1)',
                            color: this.state.fileSync ? syncColor : 'var(--jp-ui-font-color2)',
                            background: 'var(--jp-layout-color1)',
                            opacity: this.state.hovering || alwaysShowFileSync ? this.state.fileSync ? '0.87' : '0.54' : '0',
                        }} />
                    ))}
                </DIV>
                <DIV
                    sx={{
                        width: '100%',
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                        display: 'inline-flex',
                    }}
                >
                    <DirListingItemIcon
                        fileType={this.props.file.type}
                        mimetype={this.props.file.mimetype}
                        sx={{marginRight: '0px', opacity: this.state.fileSync ? '0.87' : '0.54'}}
                    />
                    <DIV
                        sx={{
                            margin: 'auto 0px',
                            overflow: 'hidden', 
                            color: this.state.fileSync ? 'var(--jp-ui-font-color1)' : 'var(--jp-ui-font-color2)', // this.props.noLongerExists ? Colors.ERROR : ''
                        }}
                        title={
                            (this.props.file.path.includes('/') ? (
`Name: ${this.props.file.path.split('/').pop()}
Path: ${this.props.file.path.replace(/\/[^\/]*$/, '/')}`
                            ) : (
`Name: ${this.props.file.path.split('/').pop()}`
                            ))
                        }
                    >
                        <DIV sx={{
                            direction: 'rtl',
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis', 
                            whiteSpace: 'nowrap',
                        }}>
                            {Global.convertOptumiPathToJupyterPath(this.props.file.path)}
                        </DIV>
                    </DIV>
                </DIV>
            </DIV>
        );
    }

    private handleFilesChanged = () => this.forceUpdate();

    public componentDidMount = () => {
        this._isMounted = true
        Global.user.fileTracker.getFilesChanged().connect(this.handleFilesChanged)
    }

    public componentWillUnmount = () => {
        Global.user.fileTracker.getFilesChanged().disconnect(this.handleFilesChanged)
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

    public shouldComponentUpdate = (nextProps: RFProps, nextState: RFState): boolean => {
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
