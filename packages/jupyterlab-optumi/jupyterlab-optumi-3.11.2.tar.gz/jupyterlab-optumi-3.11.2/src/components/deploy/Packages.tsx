/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';
import { Button } from '@mui/material';
import { withStyles } from '@mui/styles';

import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { UploadConfig } from '../../models/UploadConfig';
import { TextBox } from '../../core';

const StyledButton = withStyles({
    root: {
        height: '20px',
        padding: '0px',
        fontSize: '12px',
        lineHeight: '12px',
        minWidth: '0px',
        margin: '0px 6px 6px 6px',
        width: '100%',
    },
    label: {
        height: '20px',
    },
 })(Button);

interface IProps {
    sx?: SxProps<Theme>
}

interface IState {}

export class Packages extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super(props)
        this.state = {}
    }

    private getRequirementsValue = () => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        return uploads.requirements;
    }

    private saveRequirements = (value: string): string => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        uploads.requirements = value.replace(' ', '');
        tracker.setMetadata(optumi);
        return '';
    }

    private autoAddPackages = () => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const uploads: UploadConfig = optumi.config.upload;
        const requirements = uploads.requirements;
        const newRequirements = OptumiMetadataTracker.autoAddPackages(requirements, Global.tracker.currentWidget.content.model);
        if (newRequirements != requirements) {
            uploads.requirements = newRequirements;
            tracker.setMetadata(optumi);
        } 
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const optumi = Global.metadata.getMetadata().config;
		return (
            <>
                <DIV sx={{width: '100%'}}>
                    <DIV sx={{width: '100%', display: 'inline-flex'}}>
                        <DIV sx={{width: '50%', display: 'inline-flex'}}>
                            <StyledButton
                                onClick={this.autoAddPackages}
                                variant='contained'
                                disableElevation
                                color='primary'
                            >
                                Auto add
                            </StyledButton>
                        </DIV>
                        <DIV sx={{width: '50%', display: 'inline-flex'}} />
                    </DIV>
                    <TextBox<string>
                        key={optumi.upload.requirements}
                        multiline
                        getValue={this.getRequirementsValue}
                        saveValue={this.saveRequirements}
                        placeholder={'package==version'}
                        sx={{padding: '0px 0px 6px 0px'}}
                    />
                </DIV>
            </>
		);
	}

    private handleThemeChange = () => this.forceUpdate()
    private handleMetadataChange = () => this.forceUpdate()

    public componentDidMount = () => {
		this._isMounted = true;
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.labShell.currentChanged.connect(this.handleMetadataChange)
	}

	public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.labShell.currentChanged.disconnect(this.handleMetadataChange)
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
