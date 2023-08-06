/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, P, SPAN, StyledAccordion, StyledAccordionDetails, StyledAccordionSummary } from '../../Global';

import { SxProps, Theme } from '@mui/system';
import { IconButton } from '@mui/material';
import { ExpandMore, WarningRounded } from '@mui/icons-material';

import { SubHeader } from '../../core';
import { NotificationsPopup } from './NotificationsPopup';
import { InfoPopup } from '../../core/InfoPoppup';
import { Packages } from './Packages';
import ExtraInfo from '../../utils/ExtraInfo';
import { DataSources } from './Files';
import { EnvironmentVariables } from './EnvironmentVariables';
// import { EmbeddedYoutube } from '../../core/EmbeddedYoutube';

// const emDirNotFile = 'Path is a directory, not a file'
// const emDupPath = 'Duplicate file or directory'
// const emNoPath = 'Unable to find file or directory'

interface IProps {
    sx?: SxProps<Theme>
}

interface IState {}

export class FilesPanel extends React.Component<IProps, IState> {
    private _isMounted = false

    timeout: NodeJS.Timeout

    constructor(props: IProps) {
        super(props)
        this.state = {}
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const optumi = Global.metadata.getMetadata().config;
        const files = optumi.upload.files;
        const dataConnectors = optumi.dataConnectors;
        const fileChecker = Global.user.fileChecker;
        const [yellowTriangle, redTriangle] = fileChecker.getTriangle(files, dataConnectors);
        return (
            <DIV sx={this.props.sx}>
                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.packagesAccordionExpanded}
                    sx={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary sx={{cursor: 'default'}}>
                        <DIV sx={{display: 'flex'}}>
                            <SubHeader title='Packages'/>
                            <InfoPopup
                                title='Packages'
                                popup={
                                    <DIV sx={{margin: '12px'}}>
                                        <P sx={{whiteSpace: 'pre-line'}}>
                                            {`List Python packages that your notebook imports. Optumi will pip install these packages onto the machine your session or job will run on.

                                            Each package should go on a separate line:`}
                                        </P>
                                        <img src="https://drive.google.com/uc?export=view&id=1WePvBvaS_6xgvrljKSp8iaijlnD9MFxL" width="350" />
                                        <P sx={{whiteSpace: 'pre-line'}}>
                                            {`
                                            To save time you can hit the “Auto-add” button. Optumi will scan your notebook for imported packages and list them for you. However, this is a beta feature and we encourage you to double check that the list is correct.
                                            `}
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
                            opacity: Global.packagesAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {(() => {
                                const requirements = optumi.upload.requirements
                                const numRequirements = requirements === '' ? 0 : requirements.split('\n').filter(line => line !== '').length

                                if (numRequirements > 1) return numRequirements + ' requirements';
                                if (numRequirements > 0) return '1 requirement';
                                return ''
                            })()}
                        </SPAN>
                        <IconButton
                            size='large'
                            onClick={() => {
                                Global.packagesAccordionExpanded = !Global.packagesAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            sx={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.packagesAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <Packages />
                    </StyledAccordionDetails>
                </StyledAccordion>

                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.environmentVariablesAccordionExpanded}
                    sx={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary sx={{cursor: 'default'}}>
                        <DIV sx={{display: 'flex'}}>
                            <SubHeader title='Environment variables'/>
                            <InfoPopup
                                title='Environment variables'
                                popup={
                                    <DIV sx={{margin: '12px'}}>
                                        <P sx={{whiteSpace: 'pre-line'}}>
                                        {"Environment variables are stored encrypted in the Optumi platform and are a convenient way of accessing credentials or configuration options. You can read more about environment variables in python "}
                                        <a href='https://docs.python.org/3/library/os.html#os.environ' target='_blank' style={{marginLeft: '3px', color: 'var(--jp-ui-font-color0)', textDecoration: 'underline'}}>
                                            here
                                        </a>
                                        </P>
                                    </DIV>
                                }
                            />
                        </DIV>
                        <SPAN sx={{
                            margin: 'auto 8px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: Global.environmentVariablesAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {(() => {
                                const environmentVariables = optumi.environmentVariables
                                if (environmentVariables.length > 1) return environmentVariables.length + ' variables';
                                if (environmentVariables.length > 0) return '1 variable';
                                return ''
                            })()}
                        </SPAN>
                        <IconButton
                            size='large'
                            onClick={() => {
                                Global.environmentVariablesAccordionExpanded = !Global.environmentVariablesAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            sx={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.environmentVariablesAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <EnvironmentVariables />
                    </StyledAccordionDetails>
                </StyledAccordion>

                <StyledAccordion
                    variant={'outlined'}
                    expanded={Global.filesAccordionExpanded}
                    sx={{background: 'var(--jp-layout-color1)'}}
                >
                    <StyledAccordionSummary sx={{cursor: 'default'}}>
                        <DIV sx={{display: 'flex'}}>
                            <SubHeader title='Data sources'/>
                            <InfoPopup
                                title='Data sources'
                                popup={
                                    <DIV sx={{margin: '12px'}}>
                                        <P sx={{whiteSpace: 'pre-line'}}>
                                            {`Upload local files and access data from supported databases. Optumi will transfer files to the machine your session or job will run on.`}
                                        </P>
                                        <img src="https://drive.google.com/uc?export=view&id=1scH_eNAfnI5ivkEGfq30fjmpOdBWBmII" width="350" />
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
                        {(yellowTriangle || redTriangle) && (
                            <ExtraInfo reminder={redTriangle ? 'Files are missing, both locally and in cloud storage. Your notebook will not be able to use them.' : 'Files are missing locally. Your notebook will be able to run with files in cloud storage but we will not be able to sync them with local copies.'}>
                                <WarningRounded color={redTriangle ? 'error' : 'warning'} fontSize={'small'} sx={{marginTop: '4px', marginLeft: '6px'}} />
                            </ExtraInfo>
                        )}
                        <SPAN sx={{
                            margin: 'auto 8px',
                            flexGrow: 1,
                            textAlign: 'end',
                            opacity: Global.filesAccordionExpanded ? 0 : 0.5,
                            transitionDuration: '217ms',
                            whiteSpace: 'nowrap',
                            fontSize: '12px',
                            fontStyle: 'italic',
                        }}>
                            {files.length > 0 && (files.length + ' upload' + (files.length > 1 ? 's' : ''))}{files.length > 0 && dataConnectors.length > 0 ? ', ' : ''}{dataConnectors.length > 0 && (dataConnectors.length + ' connector' + (dataConnectors.length > 1 ? 's' : ''))}
                        </SPAN>
                        <IconButton
                            size='large'
                            onClick={() => {
                                Global.filesAccordionExpanded = !Global.filesAccordionExpanded
                                if (this._isMounted) this.forceUpdate();
                            }}
                            sx={{padding: '0px', marginRight: '-3px', width: '30px', transform: Global.filesAccordionExpanded ? 'rotate(180deg)' : undefined}}
                        >
                            <ExpandMore />
                        </IconButton>
                    </StyledAccordionSummary>
                    <StyledAccordionDetails>
                        <DataSources />
                    </StyledAccordionDetails>
                </StyledAccordion>
                <StyledAccordionSummary sx={{cursor: 'default'}}>
                    <SubHeader title='Notifications' />
                    <SPAN sx={{
                        margin: 'auto 8px',
                        flexGrow: 1,
                        textAlign: 'end',
                        opacity: 0.5,
                        transitionDuration: '217ms',
                        whiteSpace: 'nowrap',
                        fontSize: '12px',
                        fontStyle: 'italic',
                    }}>
                        {(() => {
                            let numEnabled = 0
							const config = Global.metadata.getMetadata().config
                            if (!config.interactive) {
                                const notifications = config.notifications;
                                if (notifications.jobStartedSMSEnabled) numEnabled++;
                                if (notifications.jobFailedSMSEnabled || notifications.jobCompletedSMSEnabled) numEnabled++;
                                // TODO:JJ This currently does not refresh automatically when Global.user.notificationsEnabled changes, and I wasn't sure how to quickly do this.
                                if (Global.user.notificationsEnabled && numEnabled > 0) {
                                    return numEnabled == 1 ? numEnabled + ' message' : numEnabled + ' messages'
                                }
                            }
                        })()}
                    </SPAN>
                    <NotificationsPopup onClose={() => this.forceUpdate()} disabled={Global.metadata.getMetadata().config.interactive} />
                </StyledAccordionSummary>
            </DIV>
        );
    }

	private handleLabShellChange = () => {this.forceUpdate()}
	private handleMetadataChange = () => {this.forceUpdate()}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
        Global.setLink(Global.Target.DeployTab.PackagesAccordion, () => {
            Global.packagesAccordionExpanded = true
            if (this._isMounted) this.forceUpdate();
        })
        Global.setLink(Global.Target.DeployTab.FilesAccordion, () => {
            Global.filesAccordionExpanded = true
            if (this._isMounted) this.forceUpdate();
        })
        Global.user.fileChecker.start();
		Global.labShell.currentChanged.connect(this.handleLabShellChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.user.fileChecker.stop();
        Global.labShell.currentChanged.disconnect(this.handleLabShellChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.deleteLink(Global.Target.DeployTab.PackagesAccordion)
        Global.deleteLink(Global.Target.DeployTab.FilesAccordion)
        this._isMounted = false
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
