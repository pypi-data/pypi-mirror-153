/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { withStyles } from '@mui/styles';

import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import Popover from 'react-bootstrap/Popover'

const REMOVE_EXTRA_INFO_CAUSE_ISSUE = false

// Include the bootstrap styles once
if (!REMOVE_EXTRA_INFO_CAUSE_ISSUE) document.body.innerHTML += `<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous" />`

interface ExtraInfoProps {
    children: JSX.Element,
    reminder?: string,
    overview?: string,
    documentation?: string,
    onMouseOver?: (...args: any[]) => any,
    onMouseOut?: (...args: any[]) => any,
    other?: any,
}

export default /*React.memo(*/function ExtraInfo(props: ExtraInfoProps) {
    const {
        // Props
        children,
        reminder,
        overview,
        documentation,
        onMouseOver,
        onMouseOut,
        ...other
    }: ExtraInfoProps = Object.assign({
        // Defaults
        reminder: '',
        overview: '',
        documentation: '',
    }, props)

    // To make this feel more familiar
    React.useEffect(() => { componentDidMount(); return componentWillUnmount }, [])
    const [, reRender] = React.useReducer(x => x + 1, 0)
    const forceUpdate = () => reRender()

    const componentDidMount = () => {
        Global.onInQuestionModeChange.connect(forceUpdate)
        Global.themeManager.themeChanged.connect(forceUpdate)
    }

    const componentWillUnmount = () => {
        Global.onInQuestionModeChange.disconnect(forceUpdate)
        Global.themeManager.themeChanged.disconnect(forceUpdate)
    }

    const handleMouseOver = (triggerHandler: any, ...args: any[]): any => {
        if (reminder !== undefined || (Global.inQuestionMode && overview !== undefined)) triggerHandler.onFocus(args)
        if (onMouseOver) return onMouseOver(args)
    }

    const handleMouseOut = (triggerHandler: any, ...args: any[]): any => {
        if (reminder !== undefined || (Global.inQuestionMode && overview !== undefined)) triggerHandler.onBlur(args)
        if (onMouseOut) return onMouseOut(args)
    }

    const textColor = 'var(--jp-ui-font-color1)' // 'rgba(0, 0, 0, 0.87)'
    const borderColor = 'var(--jp-ui-font-color1)' // '#0D79D4'
    const fillColor = 'var(--jp-layout-color2)' // '#D8EFFD' 

    const StyledPopover = React.useMemo(() => withStyles({
        '@global': {
            '#styled-popover *': {
                color: textColor,
                whiteSpace: 'pre-wrap',
            },
            '#styled-popover:not(:last-of-type) *': { // hides unintended popovers
                display: 'none',
            },
            '#styled-popover': {
                zIndex: `1300`,
                borderColor: borderColor,
                maxWidth: `none`,
            },
            '#styled-popover .popover-header': {
                backgroundColor: fillColor,
                borderRadius: '.3rem',
                borderBottom: 'none',
                fontWeight: Global.inQuestionMode ? 'bold' : undefined,
                fontSize: !Global.inQuestionMode ? '14px' : undefined,
                padding: !Global.inQuestionMode ? '3px 6px' : undefined,
            },
            '#styled-popover .popover-body': {
                backgroundColor: borderColor,
            },
            '#styled-popover .arrow': {
                left: !Global.inQuestionMode ? '-4px !important' : undefined, // Not sure what this is about, it didn't use to require this, then all of a sudden it did
                top: Global.inQuestionMode ? '-5px !important' : undefined,
            },
            '#styled-popover .arrow::before': {
                borderRightColor: Global.inQuestionMode ? borderColor : undefined,
                borderTopColor: !Global.inQuestionMode ? borderColor : undefined,
            },
            '#styled-popover .arrow::after': {
                borderRightColor: Global.inQuestionMode ? borderColor : undefined,
                borderTopColor: !Global.inQuestionMode ? fillColor : undefined,
                left: !Global.inQuestionMode ? undefined : (Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)) ? '1px' : '2px',
                bottom: Global.inQuestionMode ? undefined : (Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)) ? '1px' : '2px',
            },
        }
    })(Popover), [Global.inQuestionMode, Global.themeManager])

    const hasReminder = reminder !== undefined && reminder !== ''
    const hasOverview = overview !== undefined && overview !== ''

    if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
    return REMOVE_EXTRA_INFO_CAUSE_ISSUE ? children : ( // Render
        <OverlayTrigger
            delay={{show: Global.inQuestionMode ? 10 : 500, hide: 10}}
            placement={Global.inQuestionMode ? 'right' : 'top'}
            overlay={!hasReminder && !hasOverview ? (
                <StyledPopover style={{display: 'none'}} />
            ) : Global.inQuestionMode ? (
                <StyledPopover /*key={'questionMode' + reminder + overview}*/ id='styled-popover'>
                    {reminder && (
                        <Popover.Title as='h3'>
                            {reminder}
                        </Popover.Title>
                    )}
                    {overview && (
                        <Popover.Content>
                            {overview}
                        </Popover.Content>
                    )}
                </StyledPopover>
            ) : (
                <StyledPopover /*key={reminder + overview}*/ id='styled-popover'>
                    {reminder && (
                        <Popover.Title as='h3'>
                            {reminder}
                        </Popover.Title>
                    )}
                </StyledPopover>
            )}
        >
            {({ref, ...triggerHandler}) => {
                // If you can't see triggerHandler.onBlur(args), expose it in OverlayInjectedProps in node_modules/react-bootstrap/esm/OverlayTrigger.d.ts
                triggerHandler.onFocus
                triggerHandler.onBlur // Duplicate onFocus for onBlur: !!! CONTROL CLICK THIS FOR QUICK NAVIGATION TO THE FILE !!! => node_modules/react-bootstrap/esm/OverlayTrigger.d.ts:10:5
                return React.cloneElement(
                    children,
                    Object.assign({
                        ref: ref,
                        onMouseOver: (...args: any[]) => handleMouseOver(triggerHandler, args),
                        onMouseOut: (...args: any[]) => handleMouseOut(triggerHandler, args), 
                    }, {...other})
                )
            }}
        </OverlayTrigger>
    )
}/*, (props: ExtraInfoProps, nextProps: ExtraInfoProps) => {
    if (props.reminder !== nextProps.reminder) return false;
    if (props.overview !== nextProps.overview) return false;
    if (props.documentation !== nextProps.documentation) return false;
    props.children.props
    if (JSON.stringify(props.children) !== JSON.stringify(nextProps.children)) return false;
    if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
    return true
})*/
