/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { Tabs, Tab } from '@mui/material';
import { CSSProperties, withStyles } from '@mui/styles';

const StyledTab = withStyles({
    root: {
    	minHeight: "24px",
    	padding: "6px"
    }
})(Tab);

export enum Page {
	RESOURCES = 0,
	FILES = 1,
}

interface IProps {
	style?: CSSProperties
}

// Properties for this component
interface IState {
    page: Page;
}

export class RequirementsBar extends React.Component<IProps, IState> {
	_isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            page: Global.user.deploySubMenu || Page.RESOURCES,
        }
    }

	private handleTabChange = (event: React.ChangeEvent<{}>, newValue: Page) => {
        this.safeSetState({ page: newValue });
        Global.user.deploySubMenu = newValue;
	}

	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
			<DIV sx={{width: '100%', textAlign: 'center'}}>
				<Tabs 
                    value={this.state.page}
                    onChange={this.handleTabChange}
                    variant="fullWidth"
                    indicatorColor="primary"
                    textColor="primary"
                    sx={{padding: "0px 6px 0px 6px", minHeight: "24px"}}
                >
					<StyledTab
						disableRipple
                        label="RESOURCES"
                        sx={{minWidth: "100px"}}
					/>
					<StyledTab
						disableRipple
                        label="FILES"
                        sx={{minWidth: "100px"}}
					/>
				</Tabs>
			</DIV>
		);
	}

	private handleCardChange = () => this.forceUpdate()

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
		Global.user.deploySubMenuChanged.connect(this.handleCardChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.user.deploySubMenuChanged.disconnect(this.handleCardChange);
		this._isMounted = false;
	}

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
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
