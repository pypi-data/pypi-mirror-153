/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';

import { App } from '../models/application/App';
import { Header, SubHeader } from '../core';

interface IProps {
	sx?: SxProps<Theme>
}

interface IState {
	activeSessionCount: number
	activeJobCount: number
	finishedSessionCount: number
	finishedJobCount: number
}

// Defaults for this component
const DefaultState: IState = {
	activeSessionCount: 0,
	activeJobCount: 0,
	finishedSessionCount: 0,
	finishedJobCount: 0,
}

export class MonitorPage extends React.Component<IProps, IState> {
	state = DefaultState;

	private generateActive = (apps: App[]) => {
		var sorted: App[] = apps.sort((n1,n2) => {
			if (n1.timestamp > n2.timestamp) {
				return -1;
			}
			if (n1.timestamp < n2.timestamp) {
				return 1;
			}
			return 0;
		});
		return sorted.map(value => (
				<DIV key={value.uuid} sx={{padding: '6px 0px 6px 6px'}}>
					{value.getComponent()}
				</DIV>
			)
		);
	}

	private generateFinished = (apps: App[]) => {
		var sorted: App[] = apps.sort((n1,n2) => {
			if ((n1.getEndTime() || n1.timestamp) > (n2.getEndTime() ||  n2.timestamp)) {
				return -1;
			}
			if ((n1.getEndTime() || n1.timestamp) < (n2.getEndTime() ||  n2.timestamp)) {
				return 1;
			}
			return 0;
		});
		return sorted.map(value => (
				<DIV key={value.uuid} sx={{padding: '6px 0px 6px 6px'}}>
					{value.getComponent()}
				</DIV>
			)
		);
	}

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		const appTracker = Global.user.appTracker;
		return (
			<DIV sx={Object.assign({overflowY: 'auto'}, this.props.sx)}>
				<DIV sx={{padding: '6px'}}>
					<Header title="Active" />
					{this.state.activeSessionCount != 0 ? (
						<>
							<SubHeader title="Sessions" />
							{this.generateActive(appTracker.activeSessions)}
						</>
					) : (
						<DIV sx={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Sessions" grey />
							<DIV sx={{ 
									margin: '6px 0px',
									fontSize: '14px',
									lineHeight: '18px',
									opacity: 0.5
								}}>
								(none)
							</DIV>
						</DIV>
					)}
					{this.state.activeJobCount != 0 ? (
						<>
							<SubHeader title="Jobs" grey />
							{this.generateActive(appTracker.activeJobs)}
						</>
					) : (
						<DIV sx={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Jobs" grey />
							<DIV sx={{ 
								margin: '6px 0px',
								fontSize: '14px',
								lineHeight: '18px',
								opacity: 0.5
							}}>
								(none)
							</DIV>
						</DIV>
					)}
				</DIV>
				<DIV sx={{padding: '6px'}}>
					<Header title="Finished" />
					{this.state.finishedSessionCount != 0 ? (
						<>
							<SubHeader title="Sessions" grey />
							{this.generateFinished(appTracker.finishedSessions)}
						</>
					) : (
						<DIV sx={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Sessions" grey />
							<DIV sx={{ 
								margin: '6px 0px',
								fontSize: '14px',
								lineHeight: '18px',
								opacity: 0.5
							}}>
								(none)
							</DIV>
						</DIV>
					)}
					{this.state.finishedJobCount != 0 ? (
						<>
							<SubHeader title="Jobs" grey />
							{this.generateFinished(appTracker.finishedJobs)}
						</>
					) : (
						<DIV sx={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Jobs" grey />
							<DIV sx={{ 
								margin: '6px 0px',
								fontSize: '14px',
								lineHeight: '18px',
								opacity: 0.5
							}}>
								(none)
							</DIV>
						</DIV>
					)}
				</DIV>
			</DIV>
		);
	}

	private handleAppChange = () => {
		this.setState({
			activeSessionCount: Global.user?.appTracker?.activeSessions?.length || 0,
			activeJobCount: Global.user?.appTracker?.activeJobs?.length || 0,
			finishedSessionCount: Global.user?.appTracker?.finishedSessions?.length || 0,
			finishedJobCount: Global.user?.appTracker?.finishedJobs?.length || 0,
		})
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this.handleAppChange()
		Global.user.appTracker.appsChanged.connect(this.handleAppChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.user.appTracker.appsChanged.disconnect(this.handleAppChange);
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
