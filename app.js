/**
 * Author: Qingyuan Dong
 *
 * The backend (aka "server side") for AeroSpec WebApp where the all of the user and device data is stored in
 * remote Server/Database. This file also includes several endpoint which is used to access and
 * return data. If encounter problems when fetching data from server, return an error message that
 * shows it's a server error or client error.
 */
'use strict';

const express = require('express');
const app = express();
const PORT_NUM = 8080;


app.use(express.static('public'));
const PORT = process.env.PORT || PORT_NUM;
app.listen(PORT);
