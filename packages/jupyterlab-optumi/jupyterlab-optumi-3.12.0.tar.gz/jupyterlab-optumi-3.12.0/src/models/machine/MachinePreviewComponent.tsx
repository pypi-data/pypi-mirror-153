/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, SPAN } from '../../Global'

import { withStyles } from '@mui/styles';
import { SxProps, Theme } from '@mui/system';

import { Button, ButtonGroup, Dialog, DialogContent, DialogTitle, IconButton } from '@mui/material';
import { Close, MoreVert } from '@mui/icons-material';

// import { Tag } from '../../components/Tag'
// import FormatUtils from '../../utils/FormatUtils'
import { Machine, NoMachine } from './Machine'
import { Global } from '../../Global';
import { Colors } from '../../Colors';
import FormatUtils from '../../utils/FormatUtils';
import { ShadowedDivider } from '../../core';

const StyledDialog = withStyles({
    paper: {
        maxWidth: '80%',
        // height: '80%',
        overflowY: 'visible',
    },
})(Dialog);

const color = Colors.SECONDARY

const StyledButton = withStyles({
    root: {
        padding: '8px',
        // height: '28px',
        border: '1px solid ' + color + '80',
        borderRadius: '6px',
        transition: 'background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
        overflow: 'hidden',
        position: 'relative',
        fontWeight: 'normal',
        height: 'fit-content',
        color: 'var(--jp-ui-font-color1)',
    },
}) (Button)

enum Page {
    CPU = 0,
    GPU = 1,
}

interface IProps {
    machine: Machine
    sx?: SxProps<Theme>
}
interface IState {
    open: boolean,
    page: number,
    selectedMachine: string,
}

const COLUMN_WIDTH = '85px'
const FONT_SIZE = '12px'

export class MachinePreviewComponent extends React.Component<IProps, IState> {
    public _isMounted = false

    constructor(props: IProps) {
        super(props)
        const selectedMachine = Global.metadata.getMetadata().config.machineAssortment[0];
        this.state = {
            open: false,
            selectedMachine: selectedMachine,
            page: (Global.user.machines.getMachine(selectedMachine).graphicsNumCards || 0) >= 0 ? Page.GPU : Page.CPU,
        }
    }

    private handleMachineChange(machine: Machine) {
        this.safeSetState({ selectedMachine: machine.name })
        const optumi = Global.metadata.getMetadata();
        optumi.config.machineAssortment = [machine.name]
        Global.metadata.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        const machine = this.props.machine
        const machines = Global.user.machines
        return (
            <DIV sx={this.props.sx}>
                <DIV 
                    sx={{
                        display: 'inline-flex', 
                        width: '100%',
                    }}
                >
                    <DIV sx={{margin: '6px'}}>
                        {machine.getIdentityComponent()}
                        <DIV sx={{width: '100%', fontWeight: 'bold',  margin: '8px 0px 0px', fontSize: FONT_SIZE, lineHeight: FONT_SIZE, textAlign: 'center'}}>
                            Rate: {FormatUtils.styleRateUnitValue()(machine.rate || 0)}
                        </DIV>
                    </DIV>
                    <SPAN sx={{flexGrow: 1}} />
                    <DIV sx={{display: 'flex', flexDirection: 'column'}}>
                        <DIV sx={{margin: 'auto'}}>
                            {!Global.expertModeSelected && (
                                <IconButton
                                    size='large'
                                    onClick={() => {
                                        this.safeSetState({open: true})
                                    }}
                                    sx={{padding: '0px', marginRight: '-3px', width: '30px', height: '30px'}}
                                >
                                    <MoreVert sx={{height: '20px'}}/>
                                </IconButton>
                            )}
                        </DIV>
                        <DIV sx={{height: '18px'}} />
                    </DIV>
                </DIV>

                <StyledDialog
                    open={this.state.open}
                    onClose={() => {
                        this.safeSetState({open: false})
                    }}
                    scroll='paper'
                >
                    <DialogTitle
                        sx={{
                            display: 'inline-flex',
                            height: '60px',
                            padding: '6px',
                        }}
                    >
                        <DIV sx={{
                            display: 'inline-flex',
                            minWidth: '200px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <DIV sx={{margin: '12px'}}>
                                Resource selection
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1, margin: 'auto', display: 'inline-flex'}}>
                            <ButtonGroup
                                disableElevation
                                sx={{margin: 'auto', width: 'fit-content'}}>
                                <Button
                                    sx={{fontSize: '15px', padding: '5px 15px', fontWeight: 'normal'}}
                                    color='primary' variant={this.state.page == Page.CPU ? 'contained' : 'outlined'}
                                    onClick={() => this.safeSetState({ page: Page.CPU })}
                                >CPU</Button>
                                <Button
                                    sx={{fontSize: '15px', padding: '5px 15px', fontWeight: 'normal'}}
                                    color='primary' variant={this.state.page == Page.GPU ? 'contained' : 'outlined'}
                                    onClick={() => this.safeSetState({ page: Page.GPU })}
                                >GPU</Button>
                            </ButtonGroup>
                            {/* <Tabs
                                value={this.state.page}
                                onChange={(event: React.ChangeEvent<{}>, newValue: Page) => this.safeSetState({ page: newValue })}
                                variant="fullWidth"
                                indicatorColor="primary"
                                textColor="primary"
                                sx={{margin: 'auto', width: 'fit-content'}}
                            >
                                <Tab
                                    disableRipple
                                    label='CPU' sx={{minWidth: "72px"}} />
                                <Tab
                                    disableRipple
                                    label='GPU' sx={{minWidth: "72px"}} />
                            </Tabs> */}
                        </DIV>
                        <DIV sx={{minWidth: '200px', display: 'inline-flex'}}>
                            <SPAN sx={{flexGrow: 1}}/>
                            <IconButton
                                onClick={() => this.safeSetState({ open: false })}
                                sx={{
                                    display: 'inline-block',
                                    width: '36px',
                                    height: '36px',
                                    padding: '3px',
                                    margin: '6px',
                                }}
                            >
                                <Close
                                    sx={{
                                        width: '30px',
                                        height: '30px',
                                        padding: '3px',
                                    }}
                                />
                            </IconButton>
                        </DIV>
                    </DialogTitle>
                    <ShadowedDivider />
                    <DialogContent sx={{
                        padding: '0px',
                        marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
                        // lineHeight: 'var(--jp-code-line-height)',
                        fontSize: 'var(--jp-ui-font-size1)',
                        fontFamily: 'var(--jp-ui-font-family)',
                    }}>
                        <DIV sx={{height: '100%', width: 'min-content', overflow: 'auto', padding: '20px', minHeight: '875px'}}>
                            {this.state.page == Page.GPU ? (
                                <>
                                    <DIV sx={{
                                        width: '100%',
                                        display: 'inline-flex'
                                    }}>
                                        <DIV sx={{width: COLUMN_WIDTH, margin: 'auto 12px'}} />
                                        <DIV sx={{margin: 'auto 12px', display: 'inline-flex', flexGrow: 1}}>
                                            {machines.gpuLabels[0].map(l => (
                                                <DIV sx={{margin: '18px', flexGrow: 1, fontWeight: 'bold', textAlign: 'center'}}>
                                                    {l}
                                                </DIV>
                                            ))}
                                        </DIV>
                                    </DIV>
                                    {machines.gpuGrid.map((row, i) => (
                                        <>
                                            <DIV sx={{
                                                // width: '100%', 
                                                display: 'inline-flex'
                                            }}>
                                                <DIV sx={{fontWeight: 'bold', margin: 'auto 12px', textAlign: 'center', width: COLUMN_WIDTH}}>
                                                    {machines.gpuLabels[1][i]}
                                                </DIV>
                                                <DIV sx={{
                                                    // width: '100%', 
                                                    margin: '6px 12px'
                                                }}>
                                                    <DIV sx={{
                                                        // width: '100%', 
                                                        display: 'inline-flex'
                                                    }}>
                                                        {row.map((bucket) => (
                                                            <DIV sx={{
                                                                width: 'min-content', 
                                                                padding: '6px 9px',
                                                            }}>
                                                                {bucket.map((m) => (
                                                                    <DIV sx={{
                                                                        padding:  !(m instanceof NoMachine) && this.state.selectedMachine == m.name ? '5px 8px' : '6px 9px',
                                                                    }}>
                                                                        <StyledButton
                                                                            id={m.name}
                                                                            style={{
                                                                                display: 'block', 
                                                                                border: !(m instanceof NoMachine) && this.state.selectedMachine == m.name ? '2px solid ' + color : '',
                                                                            }}
                                                                            sx={{backgroundColor: !(m instanceof NoMachine) && this.state.selectedMachine == m.name ? color + '40' : '',}}
                                                                            onClick={() => this.handleMachineChange(m)}
                                                                            disabled={m instanceof NoMachine}
                                                                        >
                                                                            {m instanceof NoMachine ? <DIV sx={{height: '68px', width: '262px'}}/> : (
                                                                                <>
                                                                                    {m.getIdentityComponent()}
                                                                                    <DIV sx={{width: '100%', fontWeight: 'bold',  margin: '8px 0px 0px', fontSize: FONT_SIZE, lineHeight: FONT_SIZE, textAlign: 'center'}}>
                                                                                        Rate: {FormatUtils.styleRateUnitValue()(m.rate || 0)}
                                                                                    </DIV>
                                                                                </>
                                                                            )}
                                                                        </StyledButton>
                                                                    </DIV>
                                                                ))}
                                                            </DIV>
                                                        ))}
                                                    </DIV>
                                                </DIV>
                                            </DIV>
                                        </>
                                    ))}
                                </>
                            ) : (
                                <>
                                    <DIV sx={{
                                        width: '100%',
                                        display: 'inline-flex'
                                    }}>
                                        <DIV sx={{width: COLUMN_WIDTH, margin: 'auto 12px'}} />
                                        <DIV sx={{margin: 'auto 12px', display: 'inline-flex', flexGrow: 1}}>
                                            {machines.cpuLabels[0].map(l => (
                                                <DIV sx={{margin: '18px', flexGrow: 1, fontWeight: 'bold', textAlign: 'center'}}>
                                                    {l}
                                                </DIV>
                                            ))}
                                        </DIV>
                                    </DIV>
                                    {machines.cpuGrid.map((row, i) => (
                                        <>
                                            <DIV sx={{
                                                // width: '100%', 
                                                display: 'inline-flex'
                                            }}>
                                                <DIV sx={{fontWeight: 'bold', margin: 'auto 12px', width: COLUMN_WIDTH, textAlign: 'center'}}>
                                                    {machines.cpuLabels[1][i]}
                                                </DIV>
                                                <DIV sx={{
                                                    // width: '100%', 
                                                    margin: '6px 12px'
                                                }}>
                                                    <DIV sx={{
                                                        // width: '100%', 
                                                        display: 'inline-flex'
                                                    }}>
                                                        {row.map((bucket) => (
                                                            <DIV sx={{
                                                                width: 'min-content', 
                                                                padding: '6px 9px',
                                                            }}>
                                                                {bucket.map((m) => (
                                                                    <DIV sx={{
                                                                        padding:  !(m instanceof NoMachine) && this.state.selectedMachine == m.name ? '5px 8px' : '6px 9px',
                                                                    }}>
                                                                        <StyledButton
                                                                            id={m.name}
                                                                            style={{
                                                                                display: 'block', 
                                                                                border: !(m instanceof NoMachine) && this.state.selectedMachine == m.name ? '2px solid ' + color : '',
                                                                            }}
                                                                            sx={{backgroundColor: !(m instanceof NoMachine) && this.state.selectedMachine == m.name ? color + '40' : '',}}
                                                                            onClick={() => this.handleMachineChange(m)}
                                                                            disabled={m instanceof NoMachine}
                                                                        >
                                                                            {m instanceof NoMachine ? <DIV sx={{height: '52px', width: '262px'}}/> : (
                                                                                <>
                                                                                    {m.getIdentityComponent()}
                                                                                    <DIV sx={{width: '100%', fontWeight: 'bold',  margin: '8px 0px 0px', fontSize: FONT_SIZE, lineHeight: FONT_SIZE, textAlign: 'center'}}>
                                                                                        Rate: {FormatUtils.styleRateUnitValue()(m.rate || 0)}
                                                                                    </DIV>
                                                                                </>
                                                                            )}
                                                                        </StyledButton>
                                                                    </DIV>
                                                                ))}
                                                            </DIV>
                                                        ))}
                                                    </DIV>
                                                </DIV>
                                            </DIV>
                                        </>
                                    ))}
                                </>
                            )}
                        </DIV>
                    </DialogContent>
                </StyledDialog>
            </DIV>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

	public componentWillUnmount = () => {
        this._isMounted = false
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
}
