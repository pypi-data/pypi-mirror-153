/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../Global';

interface IProps  {
    name: string
    url: string
    width: number | string
    height: number | string
}

interface IState {}

export class EmbeddedYoutube extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <iframe
                name={this.props.name}
                src={`https://www.youtube.com/embed/${this.props.url.replace(/^.*[?&]v=([^&]+).*$/, '$1')}?modestbranding=1&rel=0`}
                width={this.props.width}
                height={this.props.height}
                allowFullScreen
                frameBorder={0}
                loading={'lazy'}
            />
        );
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
