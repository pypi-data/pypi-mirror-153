# Changelog of ShareFile Web UI

- v 1.6.10 - Upload fix - bad context change detectition in fileupload component
- v 1.6.9 - Upload fixes, few default props defined
- v 1.6.8 - Upload fixes, update disk info after file delete
- v 1.6.7 - New copy methods added - CURL and Simple URL
- v 1.6.6 - GitLab and PyPi links added
- v1.6.5 - Folder is automatically created during upload if does not exists.
- v1.6.4 - Url for simple CURL upload and share file automatically via route /api/uploadandshare/  
    usage:
    ```bash
    curl -X POST -H "Content-Type: multipart/form-data" -u "admin:pass" -F "file=@FILENAME" "http://localhost:7777/api/uploadandshare/DIRECTORY"
    ```
- v1.6.3 - startup bug fix
- v1.6.2 - Url for simple CURL uploading via route /api/simpleupload/ renamed to /api/upload/  
    usage:
    ```bash
    curl -X POST -H "Content-Type: multipart/form-data" -u "admin:pass" -F "file=@FILENAME" "http://localhost:7777/api/upload/DIRECTORY"
    ``` 
- v1.6.1 - Support for simple CURL uploading via route /api/simpleupload/
- v1.6.0 - older web browsers support added
- v1.5.17 - css
- v1.5.16 - css
- v1.5.15 - upload directory fix + confing file location changed to ~/.sharefile-webui. Please rename directory ~/.fileshare to ~/.sharefile-webui
- v1.5.14 - rollback to 1.5.10
- v1.5.13 - migration setup.py fix
- v1.5.12 - 1.5.11 migration script fixed
- v1.5.11 - links in file viewer are opened on separate tab. Data APP directory renamed to ~/.sharefile-webui/
- v1.5.10 - upload up to 4GB
- v1.5.10 - upload up to 4GB
- v1.5.9 - content editor as a reference
- v1.5.8 - upload response enhancements
- v1.5.7 - dropzone file upload fix
- v1.5.6 - css
- v1.5.5 - file path encoding fixed
- v1.5.4 - file path encoding fixed
- v1.5.3 - context escaped chars fix
- v1.5.2 - context escaped chars fix
- v1.5.1 - context escaped chars fix
- v1.5.0 - react version of WEB UI
- v1.4.6 - copy method changed
- v1.4.5 - Link handling in file viewer
- v1.4.4 - screenshot, File content viewer
- v1.4.3 - Screenshot
- v1.4.0 - File editor added. Refactoring.
- v1.3.8 - responsive
- v1.3.7 - datetime of files added. Better SPA behaviour.
- v1.3.6 - directory permission handling, refactoring
- v1.3.5 - small responsive enhancements
- v1.3.2 - responsive enhancements, next responsive breakpoint, better responsive support
- v1.3.1 - large files chunk upload + responsive support
- v1.3.0 - enhancements
- v1.2.9 - various copy methods
- v1.2.8 - screenshot
- v1.2.7 - screenshot
- v1.2.6 - coloring icons by svgfilter route
- v1.2.5 - CLI inovations
- v1.2.4 - icon redesign
- v1.2.3 - font awesome icons removed -> package size reduction
- v1.2.2 - font awesome icons
- v1.2.1 - path unquote fix
- v1.2.0 - file upload, creating dirs, rename dirs and rename files added - DOC
- v1.1.2 - disk usage functionality added
- v1.1.0 - delete .. and / dir fix
- v1.0.8 - delete token fix. Copy URL button added
- v1.0.7 - doc
- v1.0.6 - fixes and and enhancements
- v1.0.5
- v1.0.4
- v1.0.3
- v1.0.2
- v1.0.1