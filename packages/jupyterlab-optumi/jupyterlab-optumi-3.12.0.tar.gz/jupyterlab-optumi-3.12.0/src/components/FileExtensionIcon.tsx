/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global, SPAN } from '../Global'

import { fileIcon, html5Icon, imageIcon, jsonIcon, markdownIcon, notebookIcon, pythonIcon, spreadsheetIcon, yamlIcon } from '@jupyterlab/ui-components'

interface FileType {
    extension: string,
    icon: JSX.Element | undefined,
    alternativeExtensions?: string[],
}

const fileTypes: FileType[] = [
    {extension: '.aac',     icon: undefined},
    {extension: '.abw',     icon: undefined},
    {extension: '.arc',     icon: undefined},
    {extension: '.avi',     icon: undefined},
    {extension: '.azw',     icon: undefined},
    {extension: '.bin',     icon: undefined},
    {extension: '.bmp',     icon: <imageIcon.react display='block'/>},
    {extension: '.bz',      icon: undefined},
    {extension: '.bz2',     icon: undefined},
    {extension: '.csh',     icon: undefined},
    {extension: '.css',     icon: undefined},
    {extension: '.csv',     icon: <spreadsheetIcon.react display='block'/>},
    {extension: '.doc',     icon: undefined},
    {extension: '.docx',    icon: undefined},
    {extension: '.eot',     icon: undefined},
    {extension: '.gz',      icon: undefined},
    {extension: '.gif',     icon: <imageIcon.react display='block'/>},
    {extension: '.html',    icon: <html5Icon.react display='block'/>, alternativeExtensions: ['.htm']},
    {extension: '.ico',     icon: <imageIcon.react display='block'/>},
    {extension: '.ics',     icon: undefined},
    {extension: '.ipynb',   icon: <notebookIcon.react display='block'/>},
    {extension: '.jar',     icon: undefined},
    {extension: '.jpeg',    icon: <imageIcon.react display='block'/>, alternativeExtensions: ['.jpg']},
    {extension: '.js',      icon: undefined},
    {extension: '.json',    icon: <jsonIcon.react display='block'/>},
    {extension: '.md',      icon: <markdownIcon.react display='block'/>},
    {extension: '.midi',    icon: undefined, alternativeExtensions: ['.mid']},
    {extension: '.mjs',     icon: undefined},
    {extension: '.mp3',     icon: undefined},
    {extension: '.mpeg',    icon: undefined},
    {extension: '.odp',     icon: undefined},
    {extension: '.ods',     icon: undefined},
    {extension: '.odt',     icon: undefined},
    {extension: '.oga',     icon: undefined},
    {extension: '.ogv',     icon: undefined},
    {extension: '.ogx',     icon: undefined},
    {extension: '.opus',    icon: undefined},
    {extension: '.otf',     icon: undefined},
    {extension: '.png',     icon: <imageIcon.react display='block'/>},
    {extension: '.pdf',     icon: undefined},
    {extension: '.php',     icon: undefined},
    {extension: '.ppt',     icon: undefined},
    {extension: '.pptx',    icon: undefined},
    {extension: '.py',      icon: <pythonIcon.react display='block'/>},
    {extension: '.rar',     icon: undefined},
    {extension: '.rtf',     icon: undefined},
    {extension: '.sh',      icon: undefined},
    {extension: '.svg',     icon: <imageIcon.react display='block'/>},
    {extension: '.swf',     icon: undefined},
    {extension: '.tar',     icon: undefined},
    {extension: '.tiff',    icon: <imageIcon.react display='block'/>, alternativeExtensions: ['.tif']},
    {extension: '.ts',      icon: undefined},
    {extension: '.ttf',     icon: undefined},
    {extension: '.txt',     icon: undefined},
    {extension: '.vsd',     icon: undefined},
    {extension: '.wav',     icon: undefined},
    {extension: '.woff',    icon: undefined},
    {extension: '.woff2',   icon: undefined},
    {extension: '.xhtml',   icon: undefined},
    {extension: '.xls',     icon: <spreadsheetIcon.react display='block'/>},
    {extension: '.xlsx',    icon: <spreadsheetIcon.react display='block'/>},
    {extension: '.xml',     icon: undefined, alternativeExtensions: undefined},
    {extension: '.xul',     icon: undefined},
    {extension: '.yaml',    icon: <yamlIcon.react display='block'/>, alternativeExtensions: ['.yml']},
    {extension: '.zip',     icon: undefined},
    {extension: '.3gp',     icon: undefined, alternativeExtensions: undefined},
    {extension: '.3g2',     icon: undefined, alternativeExtensions: undefined},
    {extension: '.7z',      icon: undefined},
]

interface IProps {
   path: string
}

interface IState {}

export default class FileExtensionIcon extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const extension = '.' + this.props.path.split('.').pop();

        return (
            <SPAN className='jp-DirListing-itemIcon'>
                {(() => {
                    for (const fileType of fileTypes) {
                        if (fileType.extension === extension) return fileType.icon || <fileIcon.react display='block'/>
                        if (fileType.alternativeExtensions !== undefined) {
                            for (const alternativeExtension of fileType.alternativeExtensions) {
                                if (alternativeExtension === extension) return fileType.icon || <fileIcon.react display='block'/>;
                            }
                        }
                    }
                    return <fileIcon.react display='block'/>
                })()}
            </SPAN>
        )
    }
}