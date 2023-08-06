/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ServerConnection } from '@jupyterlab/services';

import { FileMetadata } from '../components/deploy/fileBrowser/FileBrowser';

export default class FileServerUtils {
	// Return two booleans, the first is if the path exists, the second is if it is a file (true) or directory (false)
	public static async checkIfPathExists(filePath: string): Promise<boolean[]> {
		const splitPath = filePath.split("/");
		let path = "";
		for (let i = 0; i < splitPath.length-1; i++) {
			path += splitPath[i]
			if (i != splitPath.length-2) {
				path += "/"
			}
		}
		const fileName = splitPath[splitPath.length-1]
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "api/contents/" + path;
		const response = ServerConnection.makeRequest(
			url, 
			{}, 
			settings
		).then((response: Response) => {
			if (response.status !== 200) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		})
		try {
			const body = (await response);
			return [body.content.some((x: any) => x.name === fileName), body.content.some((x: any) => x.name == fileName && x.type != 'directory')];
		} catch (e) {
			// If we can't find the file, the second value is invalid
			return [false, undefined]
		}
	}

	public static async getRecursiveTree(fileName: string): Promise<FileMetadata[]> {
		var files: FileMetadata[] = [];
		try {
			const settings = ServerConnection.makeSettings();
			const url = settings.baseUrl + "api/contents/" + fileName;
			const response = ServerConnection.makeRequest(
				url, 
				{}, 
				settings
			).then((response: Response) => {
				if (response.status !== 200 && response.status !== 201) {
					throw new ServerConnection.ResponseError(response);
				}
				return response.json();
			});
			const body = (await response);

			if (body.type == 'directory') {
				const promises: Promise<FileMetadata[]>[] = [];
				for (var file of body.content) {
					if (file.type == 'directory') {
						// TODO:JJ This is a problem when we have a large number of files
						promises.push(this.getRecursiveTree(file.path));
					} else {
						files.push(file as FileMetadata);
					}
				}
				for (var promise of promises) {
					files = files.concat(await promise);
				}
			} else {
				files.push(body as FileMetadata);
			}
		} catch ( err) {
			console.warn("Encountered error wile getting directory contents for " + fileName)
			console.warn(err)
		}
		return files;
	}

	public static async saveFile(filePath: string, content: string): Promise<boolean> {
		const splitPath = filePath.split("/");
		let path = "";
		for (let i = 0; i < splitPath.length-1; i++) {
			path += splitPath[i]
			if (i != splitPath.length-2) {
				path += "/"
			}
		}
		
		var builtPath = '';
		for (let dir of path.split('/')) {
			builtPath += '/' + dir
			const settings = ServerConnection.makeSettings();
			const url = settings.baseUrl + "api/contents" + builtPath;
			const body = (await ServerConnection.makeRequest(
				url, 
				{
					body: JSON.stringify({
						'path': builtPath.substring(1),
						'type': 'directory',
					}),
					method: 'PUT'
				}, 
				settings
			).then(response => {
				if (response.status !== 200 && response.status !== 201) {
					throw new ServerConnection.ResponseError(response);
				}
				return response.json();
			}));

			if (!body) return false;
		}

		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "api/contents/" + filePath;
		const response = ServerConnection.makeRequest(
			url, 
			{
				body: JSON.stringify({
					content: content,
					'format': 'text',
					'type': 'file',
				}),
				method: 'PUT'
			}, 
			settings
		).then(response => {
			if (response.status !== 200 && response.status !== 201) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		});
		const body = (await response);
		if (body) return true;
		return false;
	}

	public static async saveNotebook(filePath: string, notebook: any): Promise<boolean> {
		const splitPath = filePath.split("/");
		let path = "";
		for (let i = 0; i < splitPath.length-1; i++) {
			path += splitPath[i]
			if (i != splitPath.length-2) {
				path += "/"
			}
		}
		
		var builtPath = '';
		for (let dir of path.split('/')) {
			builtPath += '/' + dir
			const settings = ServerConnection.makeSettings();
			const url = settings.baseUrl + "api/contents" + builtPath;
			const body = (await ServerConnection.makeRequest(
				url, 
				{
					body: JSON.stringify({
						'path': builtPath.substring(1),
						'type': 'directory',
					}),
					method: 'PUT'
				}, 
				settings
			).then(response => {
				if (response.status !== 200 && response.status !== 201) {
					throw new ServerConnection.ResponseError(response);
				}
				return response.json();
			}));

			if (!body) return false;
		}

		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "api/contents/" + filePath;
		const response = ServerConnection.makeRequest(
			url, 
			{
				body: JSON.stringify({
					content: notebook,
					'format': 'json',
					'type': 'notebook',
				}),
				method: 'PUT'
			}, 
			settings
		).then(response => {
			if (response.status !== 200 && response.status !== 201) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		});
		const body = (await response);
		if (body) return true;
		return false;
	}

	public static sortFiles = (n1: FileMetadata,n2: FileMetadata) => {
		if (n1.path > n2.path) return 1;
		if (n1.path < n2.path) return -1;
		if (n1.last_modified && n2.last_modified) {
			if (new Date(n1.last_modified).getTime() < new Date(n2.last_modified).getTime()) return 1;
			if (new Date(n1.last_modified).getTime() > new Date(n2.last_modified).getTime()) return -1;
		}
		return 0;
	}
}
