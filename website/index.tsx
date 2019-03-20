import React, {Fragment} from "react";
import ReactDOM from "react-dom";
import {createGlobalStyle} from "styled-components";

import {Board} from "./components/board";
import {Title} from "./components/title";
import {Counter} from "./components/counter";

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

const App: React.StatelessComponent = () => (
    <Fragment>
        <GlobalStyle />
        <Counter
            result={async () =>
                new Promise<number>((r) => setTimeout(r.bind(null, 25), 500))
            }
        />
        <Title />
        <Board />
    </Fragment>
);

ReactDOM.render(<App />, document.getElementById("root"));
