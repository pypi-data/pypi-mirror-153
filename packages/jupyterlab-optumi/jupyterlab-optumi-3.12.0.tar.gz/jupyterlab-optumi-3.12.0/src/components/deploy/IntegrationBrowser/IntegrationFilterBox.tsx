/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SPAN } from '../../../Global';

import { SxProps, Theme } from '@mui/system';

interface IProps {
    onChange: (filter: string) => void
    sx?: SxProps<Theme>
}

interface IState {}

export default class DataConnectorFilterBox extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV className='jp-FileBrowser-filterBox' sx={this.props.sx}>
                <DIV className='bp3-input-group jp-InputGroup'>
                    <input
                        type='text'
                        placeholder='Filter connectors by name'
                        className='bp3-input'
                        style={{paddingRight: '0px'}}
                        onChange={(event) => this.props.onChange(event.currentTarget.value)}
                    />
                    <SPAN className='bp3-input-action'>
                        <DIV className='jp-InputGroupAction'>
                            <DIV>
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 18" width="16" data-icon="ui-components:search">
                                    <g xmlns="http://www.w3.org/2000/svg" className="jp-icon3" fill="#616161">
                                        <path d="M12.1,10.9h-0.7l-0.2-0.2c0.8-0.9,1.3-2.2,1.3-3.5c0-3-2.4-5.4-5.4-5.4S1.8,4.2,1.8,7.1s2.4,5.4,5.4,5.4 c1.3,0,2.5-0.5,3.5-1.3l0.2,0.2v0.7l4.1,4.1l1.2-1.2L12.1,10.9z M7.1,10.9c-2.1,0-3.7-1.7-3.7-3.7s1.7-3.7,3.7-3.7s3.7,1.7,3.7,3.7 S9.2,10.9,7.1,10.9z" />
                                    </g>
                                </svg>
                            </DIV>
                        </DIV>
                    </SPAN>
                </DIV>
            </DIV>
        )
    }
}