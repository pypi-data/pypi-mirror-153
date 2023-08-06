/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';

import { DataConnectorMetadata, IntegrationType } from './IntegrationBrowser/IntegrationBrowser';
import IntegrationDirListingItem from './IntegrationBrowser/IntegrationDirListingItem';
import { DataService } from './IntegrationBrowser/IntegrationDirListingItemIcon';
import { Colors } from '../../Colors';

interface IProps {
    dataService: DataService;
    description?: string;
    handleClick?: () => any;
    sx?: SxProps<Theme>;
}

interface IState {}

export class DataConnectorIdentity extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({}, this.props.sx)}>
                <IntegrationDirListingItem
                        key={this.props.dataService}
                        integrationMetadata={{
                            integrationType: IntegrationType.DATA_CONNECTOR,
                            name: this.props.description,
                            dataService: this.props.dataService,
                        } as DataConnectorMetadata}
                        selected={false}
                        handleButtonClick={this.props.handleClick}
                        buttonText='Create'
                        buttonColor={Colors.PRIMARY}
                        onClick={() => false}
                        onDoubleClick={() => false}
                    />
            </DIV>
            // <DIV sx={{margin: '6px'}}>
            //     <DIV sx={{display: 'inline-flex', width: '100%', height: '40px'}}>
            //         <DIV className={this.props.iconClass} sx={{width: '30px', margin: '6px 6px 6px 12px'}}/>
            //         <DIV sx={{margin: 'auto 6px', lineHeight: '14px', width: this.props.description && '92px'}}>
            //             <DIV sx={{fontWeight: 'bold'}}>
            //                 {this.props.provider}
            //             </DIV>
            //             {this.props.service != '' && (
            //                 <DIV>
            //                     {this.props.service}
            //                 </DIV>
            //             )}
            //         </DIV>
            //         {this.props.description && <DIV sx={{flexGrow: 1, margin: 'auto 12px', maxWidth: '160px'}}>
            //             {this.props.description}
            //         </DIV>}
            //         {this.props.handleClick && <Button
            //             onClick={this.props.handleClick}
            //             sx={{
            //             //     padding: '6px',
            //             //     fontWeight: 'bold',
            //             //     height: '24px',
            //                 margin: 'auto 12px',
            //             }}
            //             variant='outlined'
            //             color='primary'
            //             disableElevation
            //         >
            //             Create   
            //         </Button>}
            //     </DIV>
            // </DIV>
        )
    }
}
