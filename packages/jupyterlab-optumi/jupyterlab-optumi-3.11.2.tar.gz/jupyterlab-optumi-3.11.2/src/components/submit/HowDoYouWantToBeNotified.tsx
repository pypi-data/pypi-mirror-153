// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import * as React from 'react'
// import { DIV, Global } from '../../Global';

// import { SxProps, Theme } from '@mui/system';
// import { Button, OutlinedInput, Radio } from '@mui/material';
// import { withStyles } from '@mui/styles';

// import { PhoneTextBox } from '../../core/PhoneTextBox';

// const StyledOutlinedInput = withStyles({
//     root: {
//         padding: '0px',
//         margin: '0px 3px',
//         height: '21px',
//     },
//     input: {
//         fontSize: '12px',
//         padding: '3px 6px 3px 6px',
//     },
//     adornedEnd: {
//         paddingRight: '0px',
//     },
// }) (OutlinedInput)

// enum NotifyVia {
//     EMAIL = "email",
//     TEXT = "text",
//     NONE = "don't notify me"
// }

// interface IProps {
//     sx?: SxProps<Theme>
// }

// interface IState {
//     notifyVia: NotifyVia | null,
//     email: string,
//     phoneNumber: string,
// }

// export class DoesYourNotebookRun extends React.Component<IProps, IState> {
//     _isMounted = false;

//     public constructor(props: IProps) {
//         super(props)
//         this.state = {
//             notifyVia: null,
//             email: '',
//             phoneNumber: Global.user.phoneNumber || '',
//         }
//     }

//     public render = (): JSX.Element => {
//         if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
// 		return (
//             <>
//                 {/* This is the preview */}
//                 {this.state.notifyVia !== null && (
//                     <>
//                         {Global.capitalizeFirstLetter(this.state.notifyVia)}
//                         {this.state.notifyVia === NotifyVia.EMAIL && (
//                             <>
//                                 {': ' + this.state.email}
//                             </>
//                         )}
//                         {this.state.notifyVia === NotifyVia.TEXT && (
//                             <>
//                                 {': ' + this.state.phoneNumber}
//                             </>
//                         )}
//                     </>
//                 )}

//                 {/* This is the content */}
//                 <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                     <Radio sx={{padding: '3px'}} color='primary' checked={this.state.notifyVia === NotifyVia.EMAIL} onChange={() => this.setState({ notifyVia: NotifyVia.EMAIL })}/>
//                     <DIV sx={{margin: 'auto 0px'}}>
//                         {Global.capitalizeFirstLetter(NotifyVia.EMAIL)}
//                     </DIV>
//                 </DIV>
//                 {this.state.notifyVia === NotifyVia.EMAIL && (
//                     <StyledOutlinedInput
//                         placeholder={'example@gmail.com'}
//                         fullWidth
//                         value={this.state.email}
//                         onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.safeSetState({ email: event.target.value })}
//                     />
//                 )}
//                 <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                     <Radio sx={{padding: '3px'}} color='primary' checked={this.state.notifyVia === NotifyVia.TEXT} onChange={() => this.safeSetState({ notifyVia: NotifyVia.TEXT })}/>
//                     <DIV sx={{margin: 'auto 0px'}}>
//                         {Global.capitalizeFirstLetter(NotifyVia.TEXT)}
//                     </DIV>
//                 </DIV>
//                 {this.state.notifyVia === NotifyVia.TEXT && (
//                     <PhoneTextBox
//                         getValue={() => this.state.phoneNumber}
//                         saveValue={(phoneNumber: string) => {
//                             this.safeSetState({ phoneNumber: phoneNumber });
//                         }}
//                     />
//                 )}
//                 <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                     <Radio sx={{padding: '3px'}} color='primary' checked={this.state.notifyVia === NotifyVia.NONE} onChange={() => this.safeSetState({ notifyVia: NotifyVia.NONE })}/>
//                     <DIV sx={{margin: 'auto 0px'}}>
//                     {Global.capitalizeFirstLetter(NotifyVia.NONE)}
//                     </DIV>
//                 </DIV>
//                 <DIV sx={{display: 'inline-flex'}}>
//                     <Button
//                         // onClick={() => this.safeSetState({ activeStep: 1 })}
//                         sx={{margin: '6px'}}
//                     >
//                         Back
//                     </Button>
//                     <Button
//                         variant="contained"
//                         color="primary"
//                         // onClick={() => this.safeSetState({ activeStep: 3 })}
//                         sx={{margin: '6px'}}
//                         disabled={this.state.notifyVia === null || (this.state.notifyVia === NotifyVia.EMAIL && this.state.email === '') || (this.state.notifyVia === NotifyVia.TEXT && this.state.phoneNumber === '')}
//                     >
//                         Next
//                     </Button>
//                 </DIV>
//             </>
// 		);
// 	}

//     private handleThemeChange = () => this.forceUpdate()
//     private handleMetadataChange = () => this.forceUpdate()

//     public componentDidMount = () => {
// 		this._isMounted = true;
//         Global.themeManager.themeChanged.connect(this.handleThemeChange);
//         Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
// 	}

// 	public componentWillUnmount = () => {
//         Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
//         Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
// 		this._isMounted = false;
// 	}

//     private safeSetState = (map: any) => {
// 		if (this._isMounted) {
// 			let update = false
// 			try {
// 				for (const key of Object.keys(map)) {
// 					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
// 						update = true
// 						break
// 					}
// 				}
// 			} catch (error) {
// 				update = true
// 			}
// 			if (update) {
// 				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
// 				this.setState(map)
// 			} else {
// 				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
// 			}
// 		}
// 	}

// 	public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
//         try {
//             if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
//             if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
//             if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
//             return false;
//         } catch (error) {
//             return true;
//         }
//     }
// }
