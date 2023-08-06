/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { Box, CircularProgress, Container, CssBaseline } from '@mui/material';
import { ThemeProvider, StyledEngineProvider, createTheme, Theme } from '@mui/material/styles';
import { withStyles, StyledComponentProps } from '@mui/styles';

import { ServerConnection } from '@jupyterlab/services';
import { IThemeManager } from '@jupyterlab/apputils';

import { User } from '../models/User';
import { OauthLogin } from './OauthLogin';
import { Pilot } from './Pilot';
import { Agreement } from './Agreement';
import { providerOptions } from '../models/Snackbar';

import { SnackbarProvider } from 'notistack';
import { Colors } from '../Colors';

declare module '@mui/styles/defaultTheme' {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface DefaultTheme extends Theme {}
}

const GlobalThemeDiv = withStyles({
	'@global': {
		':root': {
			'--ot-font-family': 'var(--jp-ui-font-family)',
			'--ot-padding': '12px',
			'--ot-padding-half': '6px',
			'--ot-margin': '12px',
			'--ot-margin-half': '6px',
			'--ot-backgroundColor': 'var(--jp-layout-color1)',
			'--ot-backgroundColor-emphasized': 'var(--jp-layout-color2)',
        },
		'button:focus': {
			outline: 'none !important',
		},
		'code': {
			color: 'var(--jp-ui-font-color1) !important',
		},
		'legend': {
			width: 'unset !important',
		}
	}
})(Box)

// Properties from parent
interface IProps extends StyledComponentProps {}

// Properties for this component
interface IState {
	initialized: boolean
	loggedIn: boolean
}

class OptumiLeftPanel extends React.Component<IProps, IState> {    
    // We need to know if the component is mounted to change state
	_isMounted = false;
    private domRoot: HTMLElement;

	private refresh = () => {
		this.theme = this.getTheme();
		this.forceUpdate()
	}

    constructor(props: IProps) {
        super(props);
        this.domRoot = document.getElementById("main");
        this.state = {
			initialized: false,
            loggedIn: false,
        }
		Colors.refresh = this.refresh;
    }

	// The contents of the component
	public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
			<DIV sx={{backgroundColor: 'var(--jp-layout-color1)', height: '100%'}}>
				<GlobalThemeDiv component='div' sx={{
					height: '100%',
					display: 'flex',
					flexFlow: 'column',
					overflow: 'hidden',
					color: 'var(--jp-ui-font-color1)',
					backgroundColor: 'var(--jp-layout-color1)',
					fontSize: 'var(--jp-ui-font-size1)',
					fontFamily: 'var(--jp-ui-font-family)',
					margin: '0px auto',
				}}>
					<CssBaseline />
					<StyledEngineProvider injectFirst>
						<ThemeProvider theme={this.theme}>
							<SnackbarProvider 
								maxSnack={5} 
								domRoot={this.domRoot} 
								classes={{
									variantSuccess: this.props.classes.success,
									variantError: this.props.classes.error,
									variantWarning: this.props.classes.warning,
									variantInfo: this.props.classes.info,
								}}
							>
								{this.state.initialized ? (
									<>
										{this.state.loggedIn && Global.version ? 
											(Global.user.unsignedAgreement ? (
												<Agreement callback={() => {
													this.forceUpdate();
													// Refresh the metadata before continuing with the login
													Global.metadata.refreshMetadata().then(() => {
														// Wait to signal the change until the metadata has been set properly
														if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
														Global.onUserChange.emit(Global.user)
													});
												}}/>
											) : (
												<Pilot />
											)
										) : (
											<OauthLogin />
										)}
									</>
								) : (
									<>
										<DIV className='jp-optumi-logo' />
										<Container style={{textAlign: 'center', display: 'inline-flex', justifyContent: 'center'}} maxWidth="xs">
											<CircularProgress size='14px'  thickness={8}/>
											<DIV sx={{paddingLeft: '6px', lineHeight: '14px'}}>
												{'Initializing...'}
											</DIV>
										</Container>
									</>
								)}
							</SnackbarProvider>
						</ThemeProvider>
					</StyledEngineProvider>
				</GlobalThemeDiv>
			</DIV>
        );
	}

	private getTheme = () => {
		var themeManager: IThemeManager = Global.themeManager;
		return createTheme({
			components: {

				////
				/// Button / Icon
				//

				MuiButton: {
					styleOverrides: {
						root: {
							textTransform: 'none',
							fontWeight: 'bold',
							height: '36px',
						},
						colorInherit: {
							color: 'var(--jp-ui-font-color2)',
							borderColor: 'var(--jp-border-color1)',
							'&:hover': {
								backgroundColor: 'rgba(0, 0, 0, 0.04)',
							},
						},
					},
					defaultProps: {
						color: 'inherit',
					},
				},
				MuiIconButton: {
					styleOverrides: {
						root: {
							color: 'var(--jp-ui-font-color2)',
						},
					},
				},
				MuiSvgIcon: {
					styleOverrides: {
						root: {
							display: 'flex',
							margin: 'auto',
						},
					},
				},

				////
				/// Popup
				//

				MuiDialog: {
					styleOverrides: {
						paper: {
							backgroundColor: 'var(--jp-layout-color1)',
							backgroundImage: 'unset',
						},
						paperWidthSm: {
							maxWidth: '650px',
						},
					},
				},
				MuiDialogTitle: {
					styleOverrides: {
						root: {
							backgroundColor: 'var(--jp-layout-color2)',
							borderRadius: '4px 4px 0px 0px',
						},
					},
				},

				////
				/// Textbox / Dropdown
				//

				MuiOutlinedInput: {
					styleOverrides: {
						root: {
							lineHeight: '1.1876em',
						},
					},
					defaultProps: {
						inputProps: {
							spellCheck: 'false',
						},
					},
				},

				////
				/// Misc
				//

				MuiTab: {
					styleOverrides: {
						root: {
							color: 'var(--jp-ui-font-color2)',
							padding: '6px 12px',
							textTransform: 'none',
							fontSize: '13px',
						},
					},
				},
				MuiBadge: {
					styleOverrides: {
						badge: {
							width: '16px',
							height: '16px',
							minWidth: '16px',
							minHeight: '16px',
							fontSize: '10px',
							top: '-3px',
							right: '2px',
						}
					}
				}
			},

			typography: {
				fontFamily: 'var(--jp-ui-font-family)',
				h1: {fontSize: 'calc(var(--jp-ui-font-size1) * 2.98598)'}, // pow(1.2, 6)
				h2: {fontSize: 'calc(var(--jp-ui-font-size1) * 2.48832)'}, // pow(1.2, 5)
				h3: {fontSize: 'calc(var(--jp-ui-font-size1) * 2.0736)'}, // pow(1.2, 4)
				h4: {fontSize: 'calc(var(--jp-ui-font-size1) * 1.728)'}, // pow(1.2, 3)
				h5: {fontSize: 'calc(var(--jp-ui-font-size1) * 1.44)'}, // pow(1.2, 2)
				h6: {fontSize: 'calc(var(--jp-ui-font-size1) * 1.2)'}, // pow(1.2, 1)
				subtitle1: {fontSize: 'var(--jp-ui-font-size1)'}, // pow(1.2, 0)
				subtitle2: {fontSize: 'var(--jp-ui-font-size1)'}, // pow(1.2, 0)
				body1: {fontSize: 'var(--jp-ui-font-size1)'}, // pow(1.2, 0)
				body2: {fontSize: 'var(--jp-ui-font-size1)'}, // pow(1.2, 0)
				button: {fontSize: 'var(--jp-ui-font-size1)'}, // pow(1.2, 0)
				caption: {fontSize: 'calc(var(--jp-ui-font-size1) * 0.833333)'}, // pow(1.2, -1)
				overline: {fontSize: 'calc(var(--jp-ui-font-size1) * 0.833333)'}, // pow(1.2, -1)
			},

			palette: {
				mode: themeManager.theme == null || themeManager.isLight(themeManager.theme) ? 'light' : 'dark',
				primary: {
					// light: will be calculated from palette.primary.main,
					main: Colors.PRIMARY,
					// dark: will be calculated from palette.primary.main,
					// contrastText: will be calculated to contrast with palette.primary.main
				},
				secondary: {
					// light: will be calculated from palette.secondary.main,
					main: Colors.SECONDARY,
					// dark: will be calculated from palette.secondary.main,
					// contrastText: will be calculated to contrast with palette.secondary.main
				},
				error: {
					// light: will be calculated from palette.error.main,
					main: Colors.ERROR,
					// dark: will be calculated from palette.error.main,
				 	// contrastText: will be calculated to contrast with palette.error.main
				 },
				 warning: {
					main: Colors.WARNING,
				 },
				 // info: {

				 // },
				 success: {
					 // light: will be calculated from palette.error.main,
					 main: Colors.SUCCESS,
					 // dark: will be calculated from palette.error.main,
					 // contrastText: will be calculated to contrast with palette.error.main
				 },
				 // Used by `getContrastText()` to maximize the contrast between
				 // the background and the text.
				 contrastThreshold: 2.2,
				 // Used by the functions below to shift a color's luminance by approximately
				 // two indexes within its tonal palette.
				 // E.g., shift from Red 500 to Red 300 or Red 700.
				 tonalOffset: 0.2,
		 	},
			spacing: 12,
		});
	}
	theme: Theme = this.getTheme();

	private handleVersionSet = () => this.forceUpdate()
	private handleUserChange = () => this.safeSetState({loggedIn: Global.user != null, initialized: true})
	private handleNullUserChange = () => this.safeSetState({loggedIn: false})

	//TODO:JJ should this be async?
	private handleThemeChange = async () => {
		this.theme = this.getTheme();
		this.forceUpdate();
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
		Global.onVersionSet.connect(this.handleVersionSet);
		Global.onNullUser.connect(this.handleNullUserChange);
		Global.onUserChange.connect(this.handleUserChange);
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/check-login";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (response.status !== 200 && response.status !== 201) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		}).then((body: any) => {
			if (body.loginFailed || body.domainFailed) {
				// We need to set this to null to signal that the first login attempt completed
				Global.user = null;
			} else {
				try {
					var user = User.handleLogin(body);
					Global.user = user;
				} catch (err) {
					console.error(err);
					Global.user = null;
				}
			}
		}, () => {
			Global.user = null;
		});
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.onVersionSet.disconnect(this.handleVersionSet);
		Global.onNullUser.disconnect(this.handleNullUserChange);
		Global.onUserChange.disconnect(this.handleUserChange);
		Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
		this._isMounted = false;
	}

	public componentDidCatch(error: Error, info: React.ErrorInfo) {
		console.error(error);
		console.info(info);
	}

	public static getDerivedStateFromError(error: Error) {
		return { loggedIn: false }
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

const StyledOptumiLeftPanel = withStyles(providerOptions)(OptumiLeftPanel);
export { StyledOptumiLeftPanel as OptumiLeftPanel };
