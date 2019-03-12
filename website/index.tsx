import React, {Fragment} from "react";
import ReactDOM from "react-dom";
import styled, {createGlobalStyle} from "styled-components";

import {Header} from "./components/header";
import {Card} from "./components/card";

const GlobalStyle = createGlobalStyle`
    html, body, #root {
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
    background-color: #232323;
    display: flex;
    height: 100%;
    width: 100%;
`;

const App: React.StatelessComponent = () => (
    <Fragment>
        <GlobalStyle />
        <Layout>
            <Header />
            <Card
                type="black"
                content="What helps Obama unwind?"
                onClick={() => console.log("black")}
            />
            <Card type="outline" content="" />
            <Card
                type="white"
                content="Daddy's credit card."
                onClick={() => console.log("white")}
            />
        </Layout>
    </Fragment>
);

ReactDOM.render(<App />, document.getElementById("root"));
