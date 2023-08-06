/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'

import { Box, SxProps, Theme } from '@mui/system';

import { ILabShell, JupyterFrontEnd } from "@jupyterlab/application";
import { IThemeManager } from "@jupyterlab/apputils";
import { IDocumentManager } from '@jupyterlab/docmanager';
import { NotebookTracker } from "@jupyterlab/notebook";
import { ServerConnection } from '@jupyterlab/services';
import { Signal } from '@lumino/signaling';

import { User } from "./models/User";
import { OptumiMetadataTracker } from "./models/OptumiMetadataTracker";
import { Snackbar } from "./models/Snackbar";
import { Machine, NoMachine } from "./models/machine/Machine";

import { SnackbarKey } from "notistack";
import { Accordion, AccordionDetails, AccordionSummary, alpha, Button, Dialog, MenuItem, Select } from '@mui/material';
import { withStyles } from '@mui/styles';
import { IntegrationMetadata } from './components/deploy/IntegrationBrowser/IntegrationBrowser';

/**
 * The method to change the extension to be a certain view
 */
type Link = () => (any | Promise<any>)

/**
 * The specifier for how we want to change the extension to look
 */
type Target = {
    parent?: Target
    link?: Link
    [key: string]: Target | Link
}

export class Global {

    // The members in Target can be for dependency (we must switch to the deploy tab before switching to expert mode) or they
    // can be for organization (the settings popup doesn't do anything to prep its children, but it makes it easier to read)
    public static readonly Target = {
        SettingsPopup: {
            PreferencesTab: {},
            LimitsTab: {},
            ConnectorsTab: {},
            IntegrationsTab: {},
            StorageTab: {},
            BillingTab: {},
        },
        DeployTab: {
            PackagesAccordion: {},
            FilesAccordion: {
                UploadPopup: {},
                ConnectorPopup: {},
            },
            NotificationsPopup: {},
            LaunchAccordion: {
                SessionMode: {},
                JobMode: {},
            },
            BasicMode: {},
            ExpertMode: {},
        },
        MonitorTab: {},
        MachinesTab: {},
    }

    /**
     * This will change the view of the extension to show the specified target
     * @param target which target to open to
     */
    public static async followLink(target: Target) {
        // If things start failing all of a sudden, the solution may be to have the links
        // only return once the setState has returned (the optional callback)

        // If we have a parent, fun their link method first
        if (target.parent) await Global.followLink(target.parent);
        // Force javascript to context switch away to allow the dom to update and
        // child link methods to be initialized before we call them
        await new Promise(resolve => resolve(0))
        // Call link if it exists, and wait for it if it is asynchronous
        if (target.link) Promise.resolve(target.link());
    }

    /**
     * Initialize a target with a method to achieve that view
     * @param target the target to setup
     * @param link the method to be run to change the view to the target
     */
    public static setLink(target: Target, link: Link) {
        target.link = link
        for (const [key, value] of Object.entries(target)) {
            if (key === 'parent' || key === 'link') continue;
            // This code will run for all child targets under 'target'
            (value as any).parent = target
        }
    }

    /**
     * Deletes the method to change to this view, presumably because the component unmounted
     * @param target the target to delete
     */
    public static deleteLink(target: Target) {
        delete target.link
        // we don't delete out children's parent because their great grandparent may be the
        // only one actually mounted, and we need to be able to find them
    }

    /**
     * Helpful function for removing all links specified under a target
     * @param target the target to delete under
     */
    public static deleteLinksUnder(target: Target) {
        for (const [key, value] of Object.entries(target)) {
            if (key === 'parent' || key === 'link') continue;
            // This code will run for all child targets under 'target'
            Global.deleteLink(value as any)
        }
    }

    public static bounceAnimation = 'all 333ms cubic-bezier(0.33, 1.33, 0.66, 1) 0s'
    public static easeAnimation = 'all 150ms ease 0s'

    public static MAX_UPLOAD_SIZE = 5 * 1024 * 1024 * 1024

    // Which public stripe key we are using
    public static stripe_key = 
        // "pk_test_51HIzv8LdDawhowJuVhTKv6KRnt72In8txUs0Dss0eT4KgFFcRfQlkWEDX9kzhAeiTjiYbxgxRvKbR6TfSJcqiD4o00irQVFdtY";
        "pk_live_51HIzv8LdDawhowJuSfMFb1yBW8F9VfK87tSAfMF2UdwTNVdaixpy7xjYUcP6d5GGWs1bDfLGEexyjbYj0dkKHJac00HMDHWhxU";

    private static emitter: Global = new Global()

    private static _version: string = undefined;
    public static get version(): string { return Global._version }
    public static set version(version: string) {
        Global._version = version
        if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
        Global._onVersionSet.emit(version);
    }

    public static get isDevVersion(): boolean { return Global._version.toLocaleLowerCase().includes('dev') }

    public static userHome: string = undefined;
    public static jupyterHome: string = undefined;

    public static convertJupyterPathToOptumiPath = (path: string) => {
        return (Global.jupyterHome + '/' + path).replace(Global.userHome, '~')
    }

    public static convertOptumiPathToJupyterPath = (path: string) => {
        return path.replace('~', Global.userHome).replace(Global.jupyterHome + '/', '')
    }

    private static _onVersionSet: Signal<Global, string> = new Signal<Global, string>(Global.emitter)
    public static get onVersionSet(): Signal<Global, string> { return Global._onVersionSet }

    private static canvas: HTMLCanvasElement = document.createElement("canvas");
    public static getStringWidth(text: string, font: string): number {
        if (text == "" || text == undefined) return 0;
        // re-use canvas object for better performance
        var context: CanvasRenderingContext2D = this.canvas.getContext("2d");
        context.font = font;
        var metrics: TextMetrics = context.measureText(text + ' ');
        return metrics.width + 1;
    }

    private static _shouldLogOnRender: boolean = false
    public static get shouldLogOnRender(): boolean { return Global._shouldLogOnRender }
    static __setShouldLogOnRender(shouldLogOnRender: boolean) {
        Global._shouldLogOnRender = shouldLogOnRender
        return 'shouldLogOnRender is now set to ' + Global._shouldLogOnRender
    }

    private static _shouldLogOnEmit: boolean = false
    public static get shouldLogOnEmit(): boolean { return Global._shouldLogOnEmit }
    static __setShouldLogOnEmit(shouldLogOnEmit: boolean) {
        Global._shouldLogOnEmit = shouldLogOnEmit
        return 'shouldLogOnEmit is now set to ' + Global._shouldLogOnEmit
    }

    private static _shouldLogOnPoll: boolean = false
    public static get shouldLogOnPoll(): boolean { return Global._shouldLogOnPoll }
    static __setShouldLogOnPoll(shouldLogOnPoll: boolean) {
        Global._shouldLogOnPoll = shouldLogOnPoll
        return 'shouldLogOnPoll is now set to ' + Global._shouldLogOnPoll
    }

    private static _shouldLogOnSafeSetState: boolean = false
    public static get shouldLogOnSafeSetState(): boolean { return Global._shouldLogOnSafeSetState }
    static __setShouldLogOnSafeSetState(shouldLogOnSafeSetState: boolean) {
        Global._shouldLogOnSafeSetState = shouldLogOnSafeSetState
        return 'shouldLogOnSafeSetState is now set to ' + Global._shouldLogOnSafeSetState
    }

    private static _inQuestionMode: boolean = false
    public static get inQuestionMode(): boolean { return Global._inQuestionMode }
    public static set inQuestionMode(inQuestionMode: boolean) {
        Global._inQuestionMode = inQuestionMode
        if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
        Global._onInQuestionModeChange.emit(inQuestionMode)
    }

    private static _jobLaunched: Signal<Global, void> = new Signal<Global, void>(Global.emitter)
    public static get jobLaunched(): Signal<Global, void> { return Global._jobLaunched }

    private static _onInQuestionModeChange: Signal<Global, boolean> = new Signal<Global, boolean>(Global.emitter)
    public static get onInQuestionModeChange(): Signal<Global, boolean> { return Global._onInQuestionModeChange }

    private static _lab: JupyterFrontEnd = undefined
    public static get lab(): JupyterFrontEnd { return Global._lab }
    public static set lab(lab: JupyterFrontEnd) { Global._lab = lab }

    private static _labShell: ILabShell = undefined
    public static get labShell(): ILabShell { return Global._labShell }
    public static set labShell(labShell: ILabShell) { Global._labShell = labShell }

    private static _themeManager: IThemeManager = undefined
    public static get themeManager(): IThemeManager { return Global._themeManager }
    public static set themeManager(themeManager: IThemeManager) { Global._themeManager = themeManager }

    private static _tracker: NotebookTracker = undefined
    public static get tracker(): NotebookTracker { return Global._tracker }
    public static set tracker(tracker: NotebookTracker) { Global._tracker = tracker }

    private static _metadata: OptumiMetadataTracker = undefined
    public static get metadata(): OptumiMetadataTracker { return Global._metadata }
    public static set metadata(metadata: OptumiMetadataTracker) {
        Global._metadata = metadata
        // if (Global._metadata.getMetadata().metadata.version === 'DEV') {
        //     (window as any).setShouldLogOnRender = Global.__setShouldLogOnRender;
        //     (window as any).setShouldLogOnEmit = Global.__setShouldLogOnEmit;
        //     (window as any).setShouldLogOnPoll = Global.__setShouldLogOnPoll;
        //     (window as any).setShouldLogOnSafeSetState = Global.__setShouldLogOnSafeSetState;
        // } else {
        //     (window as any).setShouldLogOnRender = undefined;
        //     (window as any).setShouldLogOnEmit = undefined;
        //     (window as any).setShouldLogOnPoll = undefined;
        //     (window as any).setShouldLogOnSafeSetState = undefined;
        // }
    }

    private static _docManager: IDocumentManager = undefined
    public static get docManager(): IDocumentManager { return Global._docManager }
    public static set docManager(docManager: IDocumentManager) { Global._docManager = docManager }

    private static _user: User = null // If we are logged in we will have a user, otherwise it will be null
    public static get user(): User { return Global._user }
    public static set user(user: User) {
        if (user == null && this._user != null) {
            this._user.fileTracker.stopPolling();
            this._user.fileChecker.stop();
            this._user.appTracker.stopPolling();
            this._metadata = null;
            this.snackbarClose.emit(null);
            if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
            Global._onNullUser.emit(null)
            Global.labShell.collapseLeft();
            Global.labShell.collapseRight();
        }

        // Always create a new metadata tracker
        this._metadata = new OptumiMetadataTracker(this._tracker)

        setTimeout(() => {
            Global._user = user;
            // Reset 401 counter
            Global.consecutive401s = 0;
            // Reset cached info
            Global.lastMachineRate = 0;
            Global.lastCreditsBalance = 0;
            Global.lastIntegrations = [];
            Global.lastMachine = new NoMachine();

            if (user != null && !user.unsignedAgreement) {
                // Refresh the metadata before continuing with the login
                this._metadata.refreshMetadata().then(() => {
                    // Wait to signal the change until the metadata has been set properly
                    if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
                    Global._onUserChange.emit(user)
                });
            }
            Global._onUserChange.emit(user)
        }, 1000);
    }

    private static _onNullUser: Signal<Global, User> = new Signal<Global, User>(Global.emitter)
    public static get onNullUser(): Signal<Global, User> { return Global._onNullUser }

    private static _onUserChange: Signal<Global, User> = new Signal<Global, User>(Global.emitter)
    public static get onUserChange(): Signal<Global, User> { return Global._onUserChange }

    public static agreementURL: string;

    public static snackbarEnqueue: Signal<Global, Snackbar> = new Signal<Global, Snackbar>(Global.emitter);
    public static snackbarClose: Signal<Global, SnackbarKey> = new Signal<Global, SnackbarKey>(Global.emitter);
    public static dataConnectorChange: Signal<Global, void> = new Signal<Global, void>(Global.emitter);
    public static environmentVariableChange: Signal<Global, void> = new Signal<Global, void>(Global.emitter);
    public static forcePackageIntoView: Signal<Global, void> = new Signal<Global, void>(Global.emitter);
    public static lastForceCompleted: boolean = true;

    // We will keep some state here to avoid having no information to show before a request returns
    public static lastMachineRate: number = 0;
    public static lastCreditsBalance: number = 0;
    public static lastIntegrations: IntegrationMetadata[] = [];
    public static lastMachine: Machine = new NoMachine();

    public static packagesAccordionExpanded: boolean = false
    public static environmentVariablesAccordionExpanded: boolean = false
    public static filesAccordionExpanded: boolean = false
    public static launchModeAccordionExpanded: boolean = false
    public static expertModeSelected: boolean = false

    public static dismissalTimeout: number = 1.44e+7

    private static consecutive401s = 0;

    // This function will update the consecutive 401s properly and throw exceptions if the request failed
    public static handleResponse = (response: Response, ignore: boolean = false) => {
        if (response.status == 401 || response.status == 503) {
            Global.consecutive401s++;
            if (Global.consecutive401s > 5) {
                if (Global.user != null) Global.user = null;
            }
            throw new ServerConnection.ResponseError(response);
        } else {
            if (response.status != 204 && !ignore) Global.consecutive401s = 0;
            if (response.status >= 300) throw new ServerConnection.ResponseError(response);
        } 
    }
}

export const StyledSelect = withStyles({
    root: {
        fontSize: "var(--jp-ui-font-size1)",
    },
    iconOutlined: {
        right: '0px'
    },
}) (Select)

export const StyledMenuItem = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)',
        padding: '3px 3px 3px 6px',
        justifyContent: 'center',
    },
}) (MenuItem)

export const StyledAccordion = withStyles({
    root: {
        borderWidth: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
        '&:before': {
            backgroundColor: 'unset',
        },
    },
})(Accordion)

export const StyledAccordionSummary = withStyles({
    root: {
        cursor: 'default !important',
        padding: '0px',
        minHeight: '0px',
        '&.Mui-expanded': {
            minHeight: '0px',
        },
    },
    content: {
        margin: '0px',
        '&.Mui-expanded': {
            margin: '0px',
        },
    },
    expandIcon: {
        padding: '0px',
        marginRight: '0px',
    },
})(AccordionSummary)

export const StyledAccordionDetails = withStyles({
    root: {
        display: 'flex',
        flexDirection: 'column',
        padding: '0px',
    },
})(AccordionDetails)

export const WhiteTextButton = withStyles({
	root: {
		color: '#ffffff',
        '&:hover': {
            backgroundColor: alpha('#ffffff', 0.25)
        },
    },
               
})(Button);

export const SkinnyButton = withStyles({
    root: {
        height: '20px',
        padding: '0px 6px',
        fontSize: '12px',
        lineHeight: '12px',
        minWidth: '0px',
     },
     label: {
        height: '20px',
    },
})(Button);

export const PermanentPopup = withStyles((theme: Theme) => ({
    root: {
        margin: '12px',
        padding: '0px',
    },
    paper: {
        backgroundColor: 'var(--jp-layout-color1)',
        minWidth: '640px',
    },
}))(Dialog);

interface BoxProps {
    children?: React.ReactNode
    className?: string
    dangerouslySetInnerHTML?: any
    id?: any
    onClick?: any
    onContextMenu?: any
    onDoubleClick?: any
    onMouseOut?: any
    onMouseOver?: any
    innerRef?: React.RefObject<HTMLElement>
    style?: React.CSSProperties, // legacy
    sx?: SxProps<Theme>
    title?: string
    rows?: number
    readOnly?: boolean
}

class BOX extends React.Component<BoxProps & {component: React.ElementType}> {
    render() {
        const { children, innerRef, ...other } = this.props
        return (
            <Box ref={innerRef} {...other}>
                {children}
            </Box>
        )
    }
}

export class DIV extends React.Component<BoxProps> { render = () => <BOX component='div' {...this.props} /> }
export class LI extends React.Component<BoxProps> { render = () => <BOX component='li' {...this.props} /> }
export class P extends React.Component<BoxProps> { render = () => <BOX component='p' {...this.props} /> }
export class PRE extends React.Component<BoxProps> { render = () => <BOX component='pre' {...this.props} /> }
export class SPAN extends React.Component<BoxProps> { render = () => <BOX component='span' {...this.props} /> }
export class UL extends React.Component<BoxProps> { render = () => <BOX component='ul' {...this.props} /> }
export class TEXTAREA extends React.Component<BoxProps> { render = () => <BOX component='textarea' {...this.props} /> }
