import { Router } from "express";
import { getClient } from "../auth.js";
import path from 'path';
import fs from 'fs';
import config from '../_secrets/config.js';

const configPath = path.join(path.resolve(), '_secrets/keycloak.json');
const kcConfig = JSON.parse(fs.readFileSync(configPath));
const router = Router();

router.get('/login', async (req, res, next)=>{
    let client;
    try{
        client = await getClient();
    }catch(e){
        console.log(e);
        return res.status(500).send({"error":"error contacting issuer service"})
    }
    
    const rurl = client.authorizationUrl({
        scope:kcConfig.scope,
        resource:kcConfig.resource
    });
    console.log(rurl);
    return res.redirect(rurl);
});

router.post('/login',function (req, res, next){
    console.log(req.params);
});


router.get('/user/:userid');

router.get('/profile', async (req, res, next)=>{
    const client = await getClient();
    if (req.query.code){
        try{
            const q = client.callbackParams(req)
            console.log(q, 'create container internal request');
            const token = await client.callback(config.KC_REDIRECT_URI, q);
            res.cookie('token', token.id_token);
            res.redirect(config.CLIENT);
        }catch(e){
            res.send(e);
        }
    }
    next();
});

export default router;

