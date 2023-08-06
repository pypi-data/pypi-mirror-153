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
    file: FileMetadata
    onOpen: (file: FileMetadata) => void
}

interface IState {}

export default class BreadCrumbItem extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <SPAN className='jp-BreadCrumbs-item' title={this.props.file.path} onClick={() => this.props.onOpen(this.props.file)}>
                    {this.props.file.name}
                </SPAN>
                <SPAN>/</SPAN>
            </>
        )
    }
}