import express from 'express';
import cookieParser from 'cookie-parser';
import userRouter from './users/router.js';

const app = express();
const port = 8010;
app.use(cookieParser());

app.use('/api/users/v1', userRouter);

app.listen(port, 'localhost',()=>{
    console.log(`now listening ${port}`);
});
