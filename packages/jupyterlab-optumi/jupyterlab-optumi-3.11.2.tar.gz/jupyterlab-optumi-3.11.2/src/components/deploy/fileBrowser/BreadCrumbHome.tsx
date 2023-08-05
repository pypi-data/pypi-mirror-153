/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global, SPAN } from '../../../Global';

import { FileMetadata } from './FileBrowser'

interface IProps {
    serverRoot: string
    file: FileMetadata
    onOpen: (file: FileMetadata) => void
}

interface IState {}

export default class BreadCrumbHome extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <SPAN className='jp-BreadCrumbs-home jp-BreadCrumbs-item' title={this.props.serverRoot} onClick={() => this.props.onOpen(this.props.file)}>
                    <svg width='16' viewBox='0 0 24 24' style={{
                        height: '16px',
                        bottom: '1px',
                        position: 'relative',
                        margin: '0px 2px 0px 0px',
                        padding: '0px 2px',
                        verticalAlign: 'middle'
                    }}>
                        <path className='jp-icon3 jp-icon-selectable' fill='#616161' d='M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z' />
                    </svg>
                </SPAN>
                <SPAN>/</SPAN>
            </>
        )
    }
}