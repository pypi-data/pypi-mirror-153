/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from './Global';

import {
	JupyterFrontEnd,
	JupyterFrontEndPlugin,
	ILabShell,
	ILayoutRestorer
} from '@jupyterlab/application';
import { ServerConnection } from '@jupyterlab/services';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ReactWidget, IThemeManager } from '@jupyterlab/apputils';
import { INotebookTracker, NotebookTracker } from '@jupyterlab/notebook';
import { Token } from "@lumino/coreutils";
import { Widget } from "@lumino/widgets";

import { OptumiLeftPanel } from './components/LeftPanel';

// TODO:JJ Does this really need to be exported?
export const IOptumi = new Token<IOptumi>(
	"optumi:IOptumi"
);

// TODO:JJ Does this really need to be exported?
export interface IOptumi {
	widget: Widget;
}

const id = "optumi";

export default {
	activate,
	id,
	requires: [ILabShell, ILayoutRestorer, INotebookTracker, IThemeManager, IDocumentManager],
	provides: IOptumi,
	autoStart: true
} as JupyterFrontEndPlugin<IOptumi>;

async function activate(
	lab: JupyterFrontEnd,
	labShell: ILabShell,
	restorer: ILayoutRestorer,
	tracker: INotebookTracker,
	manager: IThemeManager,
	docManager: IDocumentManager,
): Promise<IOptumi> {
	let widget: ReactWidget;

	async function loadPanel() {
		// add widget
		if (!widget.isAttached) {
			labShell.add(widget, "left", { rank: 1000 });
		}
	}
	// Creates the left side bar widget once the app has fully started
	lab.started.then(() => {
		document.documentElement.style.setProperty('--jp-sidebar-min-width', '340px');
		// Set some well known globals
		Global.lab = lab;
		Global.labShell = labShell;
		Global.themeManager = manager;
		Global.docManager = docManager;
		Global.tracker = tracker as NotebookTracker;
		docManager.services.contents.getDownloadUrl("Agreement.html").then((url: string) => Global.agreementURL = url);

		// Wait until we have a version to set metadata related globals
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'optumi/version'
		ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json()
		}).then((data: any) => {
			// Get the version from the server
			// We do not want to start the extension until we know the version, it might mess with metadata
			const version = data.version
			const userHome = data.userHome
			const jupyterHome = data.jupyterHome

			console.log('JupyterLab extension jupyterlab-optumi version ' + version + ' is activated!');

			Global.version = version
			Global.userHome = userHome
			Global.jupyterHome = jupyterHome
		});

		widget = ReactWidget.create(
			<OptumiLeftPanel />
		);
		widget.id = 'optumi/Optumi';
		widget.title.iconClass = 'jp-o-logo jp-SideBar-tabIcon';
		widget.title.caption = 'Optumi';

		restorer.add(widget, widget.id);
	});

	// Initialize once the application shell has been restored
	lab.restored.then(() => {
		loadPanel();
	});

	return {widget}
}
