/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../../Global';

import BreadCrumbEllipses from './BreadCrumbEllipses'
import BreadCrumbHome from './BreadCrumbHome'
import BreadCrumbItem from './BreadCrumbItem'
import { FileMetadata } from './FileBrowser'

interface IProps {
    serverRoot: string
    root: FileMetadata
    path: FileMetadata[]
    onOpen: (file: FileMetadata) => void
}

interface IState {}

export default class BreadCrumbs extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV className='jp-BreadCrumbs jp-FileBrowser-crumbs'>
                <BreadCrumbHome serverRoot={this.props.serverRoot} file={this.props.root} onOpen={this.props.onOpen} />
                {this.props.path.length > 2 && <BreadCrumbEllipses file={this.props.path[this.props.path.length - 3]} onOpen={this.props.onOpen} />}
                {this.props.path.length > 1 && <BreadCrumbItem file={this.props.path[this.props.path.length - 2]} onOpen={this.props.onOpen} />}
                {this.props.path.length > 0 && <BreadCrumbItem file={this.props.path[this.props.path.length - 1]} onOpen={this.props.onOpen} />}
            </DIV>
        )
    }
}