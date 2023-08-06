/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, P, SPAN, StyledAccordion, StyledAccordionDetails, StyledAccordionSummary } from '../../../Global';

import { SxProps, Theme } from '@mui/system';
import { IconButton } from '@mui/material';
import { ExpandMore } from '@mui/icons-material';

import { SubHeader } from '../../../core';
// import { EmbeddedYoutube } from '../../../core/EmbeddedYoutube';
import { InfoPopup } from '../../../core/InfoPoppup';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import ExtraInfo from '../../../utils/ExtraInfo';
import { OutlinedResourceRadio } from '../OutlinedResourceRadio';
import { Colors } from '../../../Colors';

interface IProps {
    sx?: SxProps<Theme>,
}

interface IState {}

export class LaunchMode extends React.Component<IProps, IState> {
    private _isMounted = false

    private getValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        return optumi.config.interactive ? "Session" : "Job";
	}

	private saveValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.config.interactive = value == "Session" ? true : false;
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const value = this.getValue();
        const optumi = Global.metadata.getMetadata().config;
        return (
            <DIV sx={this.props.sx}>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.launchModeAccordionExpanded}
                    sx={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary sx={{cursor: 'default'}}>
                        <DIV sx={{display: 'flex'}}>
                            <SubHeader title='Launch mode'/>
                            <InfoPopup
                                title='Launch mode'
                                popup={
                                    <DIV sx={{margin: '12px'}}>
                                        <P sx={{whiteSpace: 'pre-line'}}>
                                            {`The selected launch mode determines how your notebook will be run in the cloud.`}
                                        </P>
                                        <P sx={{whiteSpace: 'pre-line', fontWeight: 'bold', marginBottom: '0'}}>
                                            {`Session`}
                                        </P>
                                        <P sx={{whiteSpace: 'pre-line'}}>
                                            {`If selected, Optumi will start a JupyterLab server in the cloud that you will connect to with your browser. A new browser tab will open automatically when the session is ready for use. You will be able to work interactively the same way you do on your local laptop, however notebook execution will take place on the remote server.

                                            This is often useful when developing or debugging your notebook.`}
                                        </P>
                                        <P sx={{whiteSpace: 'pre-line', fontWeight: 'bold', marginBottom: '0'}}>
                                            {`Job`}
                                        </P>
                                        <P sx={{whiteSpace: 'pre-line'}}>
                                            {`If selected, Optumi will take a snapshot of your current notebook and execute it in the cloud from start to finish. You will be able to see the notebook output as your job progresses, however you won't be able to re-run individual cells within the notebook.

                                            This is often useful when training or tuning hyperparameters. You can think of it as a fire-and-forget mode where you are free to close your browser without disrupting notebook execution.`}
                                        </P>
                                        {/* <EmbeddedYoutube
                                            name='Demo'
                                            url={'https://www.youtube.com/watch?v=MXzv-XL6LLs'}
                                            width={700}
                                            height={480}
                                        /> */}
                                    </DIV>
                                }
                            />
                        </DIV>
                        <SPAN sx={{
                            margin: 'auto 8px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: Global.launchModeAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {optumi.interactive ? 'session' : 'job'}
                        </SPAN>
                        <IconButton
                            size='large'
                            onClick={() => {
                                Global.launchModeAccordionExpanded = !Global.launchModeAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            sx={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.launchModeAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <DIV
                            sx={{
                                alignItems: 'center',
                                display: 'inline-flex',
                                width: '100%',
                            }}
                        >
                            <ExtraInfo reminder='Run an interactive session'>
                                <OutlinedResourceRadio label={'Session'} color={Colors.SECONDARY} selected={value == "Session"} handleClick={() => this.saveValue("Session")}/>
                            </ExtraInfo>
                            <ExtraInfo reminder='Run a batch job'>
                                <OutlinedResourceRadio label={"Job"} color={Colors.SECONDARY} selected={value == "Job"} handleClick={() => this.saveValue("Job")}/>
                            </ExtraInfo>
                        </DIV>
                    </StyledAccordionDetails>
                </StyledAccordion>
            </DIV>
        );
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
        Global.setLink(Global.Target.DeployTab.LaunchAccordion, () => {
            Global.launchModeAccordionExpanded = true
            if (this._isMounted) this.forceUpdate();
        })
        Global.setLink(Global.Target.DeployTab.LaunchAccordion.SessionMode, () => this.saveValue('Session'))
        Global.setLink(Global.Target.DeployTab.LaunchAccordion.JobMode, () => this.saveValue('Job'))
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.deleteLink(Global.Target.DeployTab.LaunchAccordion)
        Global.deleteLinksUnder(Global.Target.DeployTab.LaunchAccordion)
        this._isMounted = false;
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
