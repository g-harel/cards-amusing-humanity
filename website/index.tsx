import React, {Fragment} from "react";
import ReactDOM from "react-dom";

import {Header} from "./components/header";

const App: React.StatelessComponent = () => (
    <Fragment>
        <Header />
    </Fragment>
);

ReactDOM.render(<App />, document.getElementById("root"));
