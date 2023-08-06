/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global, SPAN } from '../../../Global';

import { SxProps, Theme } from '@mui/system';

import { fileIcon, folderIcon, html5Icon, imageIcon, jsonIcon, markdownIcon, notebookIcon, pythonIcon, spreadsheetIcon, yamlIcon } from '@jupyterlab/ui-components'

interface FileType {
    extension: string,
    mime: string,
    icon: JSX.Element | undefined,
    alternativeExtensions?: string[],
    alternativeMimes?: string[],
}

const fileTypes: FileType[] = [
    {extension: '.aac',     mime: 'audio/aac',                      icon: undefined},
    {extension: '.abw',     mime: 'application/x-abiword',          icon: undefined},
    {extension: '.arc',     mime: 'application/x-freearc',          icon: undefined},
    {extension: '.avi',     mime: 'video/x-msvideo',                icon: undefined},
    {extension: '.azw',     mime: 'application/vnd.amazon.ebook',   icon: undefined},
    {extension: '.bin',     mime: 'application/octet-stream',       icon: undefined},
    {extension: '.bmp',     mime: 'image/bmp',                      icon: <imageIcon.react display='block'/>},
    {extension: '.bz',      mime: 'application/x-bzip',             icon: undefined},
    {extension: '.bz2',     mime: 'application/x-bzip2',            icon: undefined},
    {extension: '.csh',     mime: 'application/x-csh',              icon: undefined},
    {extension: '.css',     mime: 'text/css',                       icon: undefined},
    {extension: '.csv',     mime: 'text/csv',                       icon: <spreadsheetIcon.react display='block'/>},
    {extension: '.doc',     mime: 'application/msword',             icon: undefined},
    {extension: '.docx',    mime: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', icon: undefined},
    {extension: '.eot',     mime: 'application/vnd.ms-fontobject',  icon: undefined},
    {extension: '.gz',      mime: 'application/gzip',               icon: undefined},
    {extension: '.gif',     mime: 'image/gif',                      icon: <imageIcon.react display='block'/>},
    {extension: '.html',    mime: 'text/html',                      icon: <html5Icon.react display='block'/>, alternativeExtensions: ['.htm']},
    {extension: '.ico',     mime: 'image/vnd.microsoft.icon',       icon: <imageIcon.react display='block'/>},
    {extension: '.ics',     mime: 'text/calendar',                  icon: undefined},
    {extension: '.jar',     mime: 'application/java-archive',       icon: undefined},
    {extension: '.jpeg',    mime: 'image/jpeg',                     icon: <imageIcon.react display='block'/>, alternativeExtensions: ['.jpg']},
    {extension: '.js',      mime: 'text/javascript',                icon: undefined},
    {extension: '.json',    mime: 'application/json',               icon: <jsonIcon.react display='block'/>},
    {extension: '.md',      mime: 'text/markdown',                  icon: <markdownIcon.react display='block'/>},
    {extension: '.midi',    mime: 'audio/midi',                     icon: undefined, alternativeExtensions: ['.mid'], alternativeMimes: ['audio/x-midi']},
    {extension: '.mjs',     mime: 'text/javascript',                icon: undefined},
    {extension: '.mp3',     mime: 'audio/mpeg',                     icon: undefined},
    {extension: '.mpeg',    mime: 'video/mpeg',                     icon: undefined},
    {extension: '.odp',     mime: 'application/vnd.oasis.opendocument.presentation', icon: undefined},
    {extension: '.ods',     mime: 'application/vnd.oasis.opendocument.spreadsheet', icon: undefined},
    {extension: '.odt',     mime: 'application/vnd.oasis.opendocument.text', icon: undefined},
    {extension: '.oga',     mime: 'audio/ogg',                      icon: undefined},
    {extension: '.ogv',     mime: 'video/ogg',                      icon: undefined},
    {extension: '.ogx',     mime: 'application/ogg',                icon: undefined},
    {extension: '.opus',    mime: 'audio/opus',                     icon: undefined},
    {extension: '.otf',     mime: 'font/otf',                       icon: undefined},
    {extension: '.png',     mime: 'image/png',                      icon: <imageIcon.react display='block'/>},
    {extension: '.pdf',     mime: 'application/pdf',                icon: undefined},
    {extension: '.php',     mime: 'application/x-httpd-php',        icon: undefined},
    {extension: '.ppt',     mime: 'application/vnd.ms-powerpoint',  icon: undefined},
    {extension: '.pptx',    mime: 'application/vnd.openxmlformats-officedocument.presentationml.presentation', icon: undefined},
    {extension: '.py',      mime: 'text/x-python',                  icon: <pythonIcon.react display='block'/>},
    {extension: '.rar',     mime: 'application/vnd.rar',            icon: undefined},
    {extension: '.rtf',     mime: 'application/rtf',                icon: undefined},
    {extension: '.sh',      mime: 'application/x-sh',               icon: undefined},
    {extension: '.svg',     mime: 'image/svg+xml',                  icon: <imageIcon.react display='block'/>},
    {extension: '.swf',     mime: 'application/x-shockwave-flash',  icon: undefined},
    {extension: '.tar',     mime: 'application/x-tar',              icon: undefined},
    {extension: '.tiff',    mime: 'image/tiff',                     icon: <imageIcon.react display='block'/>, alternativeExtensions: ['.tif']},
    {extension: '.ts',      mime: 'video/mp2t',                     icon: undefined},
    {extension: '.ttf',     mime: 'font/ttf',                       icon: undefined},
    {extension: '.txt',     mime: 'text/plain',                     icon: undefined},
    {extension: '.vsd',     mime: 'application/vnd.visio',          icon: undefined},
    {extension: '.wav',     mime: 'audio/wav',                      icon: undefined},
    {extension: '.woff',    mime: 'font/woff',                      icon: undefined},
    {extension: '.woff2',   mime: 'font/woff2',                     icon: undefined},
    {extension: '.xhtml',   mime: 'application/xhtml+xml',          icon: undefined},
    {extension: '.xls',     mime: 'application/vnd.ms-excel',       icon: <spreadsheetIcon.react display='block'/>},
    {extension: '.xlsx',    mime: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', icon: <spreadsheetIcon.react display='block'/>},
    {extension: '.xml',     mime: 'application/xml',                icon: undefined, alternativeExtensions: undefined, alternativeMimes: ['text/xml']},
    {extension: '.xul',     mime: 'application/vnd.mozilla.xul+xml', icon: undefined},
    {extension: '.yaml',    mime: 'application/x-yaml',             icon: <yamlIcon.react display='block'/>, alternativeExtensions: ['.yml'], alternativeMimes: ['text/yaml']},
    {extension: '.zip',     mime: 'application/zip',                icon: undefined},
    {extension: '.3gp',     mime: 'video/3gpp',                     icon: undefined, alternativeExtensions: undefined, alternativeMimes: ['audio/3gpp']},
    {extension: '.3g2',     mime: 'video/3gpp2',                    icon: undefined, alternativeExtensions: undefined, alternativeMimes: ['audio/3gpp2']},
    {extension: '.7z',      mime: 'application/x-7z-compressed',    icon: undefined},
]

interface IProps {
    fileType: 'notebook' | 'file' | 'directory'
    mimetype: string
    sx?: SxProps<Theme>
}

interface IState {}

export default class DirListingItemIcon extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <SPAN className='jp-DirListing-itemIcon' sx={this.props.sx}>
                {this.props.fileType === 'notebook' ? (
                    <notebookIcon.react display='block'/>
                ) : this.props.fileType === 'directory' ? (
                    <folderIcon.react display='block'/>
                ) : (() => {
                    for (const fileType of fileTypes) {
                        if (fileType.mime === this.props.mimetype) return fileType.icon || <fileIcon.react display='block'/>
                        if (fileType.alternativeMimes !== undefined) {
                            for (const alternativeMime of fileType.alternativeMimes) {
                                if (alternativeMime === this.props.mimetype) return fileType.icon || <fileIcon.react display='block'/>;
                            }
                        }
                    }
                    return <fileIcon.react display='block'/>
                })()}
            </SPAN>
        )
    }
}
