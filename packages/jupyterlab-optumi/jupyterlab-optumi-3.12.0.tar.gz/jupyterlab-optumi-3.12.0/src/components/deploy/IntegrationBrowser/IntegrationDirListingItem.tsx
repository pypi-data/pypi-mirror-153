/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global, LI, SPAN } from '../../../Global';

import { Button } from '@mui/material';
import { withStyles } from '@mui/styles';

import DataConnectorDirListingItemIcon, { DataService } from './IntegrationDirListingItemIcon'
import { DataConnectorMetadata, IntegrationMetadata, IntegrationType } from './IntegrationBrowser'
import Terminal from '@mui/icons-material/Terminal';

const StyledButton = withStyles({
    root: {
        display: 'inline-block',
        height: '20px',
        padding: '3px 6px',
        lineHeight: '12px',
        fontSize: '12px',
        minWidth: '0px',
        margin: 'auto',
    },
 })(Button);

interface DataConnectorType {
   dataService: DataService,
   provider: string,
   service: string,
}

const dataConnectorTypes: DataConnectorType[] = [
    {dataService: DataService.AMAZON_S3,            provider: 'Amazon', service: 'S3'},
    {dataService: DataService.AZURE_BLOB_STORAGE,   provider: 'Azure', service: 'Blob Storage'},
    {dataService: DataService.WASABI,               provider: 'Wasabi', service: ''},
    {dataService: DataService.GOOGLE_DRIVE,         provider: 'Google', service: 'Drive'},
    {dataService: DataService.GOOGLE_CLOUD_STORAGE, provider: 'Google', service: 'Cloud Storage'},
    {dataService: DataService.KAGGLE,               provider: 'Kaggle', service: ''},
    {dataService: DataService.EMPTY,                provider: '', service: '--'},
]

interface IProps {
    integrationMetadata: IntegrationMetadata
    selected: boolean
    onClick: (event: React.MouseEvent<HTMLLIElement, MouseEvent>) => void
    onDoubleClick: (event: React.MouseEvent<HTMLLIElement, MouseEvent>) => void
    handleButtonClick?: (integrationMetadata: IntegrationMetadata) => void
    buttonColor?: string
    buttonText?: string
}

interface IState {}

export default class IntegrationDirListingItem extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
        this.state = {
            focused: false
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const integrationMetadata = this.props.integrationMetadata
        return (
            <LI
                className={'jp-DirListing-item' + (this.props.selected ? ' jp-mod-selected' : '')}
                sx={{lineHeight: '25px', padding: '4px 17px'}}
                onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => this.props.onClick(event)}
                onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => this.props.onDoubleClick(event)}
            >   
                {this.props.integrationMetadata.integrationType == IntegrationType.ENVIRONMENT_VARIABLE ? (<>
                        <Terminal
                            sx={Object.assign({
                                margin: '2.5px auto',
                                width: '20px',
                                height: '20px',
                            })}
                        />
                        <SPAN className='jp-DirListing-itemModified' 
                            sx={{ marginLeft: '8px' }}
                            style={{flex: '0 0 185px', textAlign: 'left'}}
                        >
                            <>
                                <SPAN sx={{fontWeight: 'bold', marginRight: '0.25em'}}>
                                    Environment variable
                                </SPAN>
                            </>
                        </SPAN>
                    </>
                ) : (
                    <>
                        <DataConnectorDirListingItemIcon
                            sx={{
                                margin: '2.5px auto',
                                width: '20px',
                                height: '20px',
                            }}
                            dataService={(integrationMetadata as DataConnectorMetadata).dataService} 
                        />
                        <SPAN className='jp-DirListing-itemModified' 
                            sx={
                                (integrationMetadata as DataConnectorMetadata).dataService == DataService.EMPTY ? {
                                    marginLeft: '-24px',
                                    marginRight: '24px',
                                } : {
                                    marginLeft: '8px'
                                }
                            }
                            style={{flex: '0 0 185px', textAlign: 'left'}}
                        >
                            {(() => {
                                for (const dataConnectorType of dataConnectorTypes) {
                                    if (dataConnectorType.dataService === (integrationMetadata as DataConnectorMetadata).dataService) {
                                        return (
                                            <>
                                                <SPAN sx={{fontWeight: 'bold', marginRight: '0.25em'}}>
                                                    {dataConnectorType.provider}
                                                </SPAN>
                                                {dataConnectorType.service}
                                            </>
                                        )
                                    }
                                }
                                return <SPAN />
                            })()}
                        </SPAN>
                    </>
                )}
                
                
                <SPAN className='jp-DirListing-itemText'>
                    {integrationMetadata.name}
                </SPAN>
                {this.props.handleButtonClick && this.props.buttonColor && this.props.buttonText && (
                    <StyledButton
                        onClick={() => this.props.handleButtonClick(this.props.integrationMetadata)}
                        variant='outlined'
                        color='primary'
                        disableElevation
                        sx={{
                            color: this.props.buttonColor,
                            border: '1px solid ' + this.props.buttonColor,
                        }}
                    >
                        {this.props.buttonText}
                    </StyledButton>
                )}
            </LI>
        )
    }
}
