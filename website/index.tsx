import React, {Fragment} from "react";
import ReactDOM from "react-dom";
import styled, {createGlobalStyle} from "styled-components";

import {Header} from "./components/header";
import {Board} from "./components/board";

const GlobalStyle = createGlobalStyle`
    html, body, #root {
        background-color: #232323;
        color: #ffffff;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 20px;
        font-weight: 500;
        height: 100%;
        margin: 0;
        width: 100%;
    }

    * {
        box-sizing: border-box;
    }
`;

const Layout = styled.main`
    display: flex;
    flex-wrap: wrap;
    height: 100%;
    width: 100%;
`;

const App: React.StatelessComponent = () => (
    <Fragment>
        <GlobalStyle />
        <Layout>
            <Header />
            <Board />
        </Layout>
    </Fragment>
);

ReactDOM.render(<App />, document.getElementById("root"));
