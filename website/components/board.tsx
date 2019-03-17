import React, {useState, useEffect} from "react";
import styled from "styled-components";

import {Game} from "./game";
import {CreateGame} from "../internal/endpoints";
import {IGameToken, IGameResult} from "../internal/types";

const Wrapper = styled.div`
    display: flex;
    flex-flow: wrap;
    padding: 1rem 1rem 3rem;
    height: 100%;
`;

interface State {
    game?: IGameToken;
    result?: IGameResult;
}

export const Board: React.FunctionComponent = () => {
    const [state, setState] = useState<State>({});

    useEffect(() => {
        CreateGame.call({}).then((game) => setState({game}));
    }, []);

    return (
        <Wrapper>
            {state.game && (
                <Game
                    black={{
                        id: "b1",
                        description: "What gets better with age?",
                    }}
                    white={[
                        {id: "w1", description: "Daddy's credit card."},
                        {id: "w2", description: "Drinking alone."},
                        {id: "w3", description: "The glass ceiling."},
                        {id: "w4", description: "A lifetime of sadness."},
                        {id: "w5", description: "A PowerPoint presentation."},
                    ]}
                    onPick={console.log}
                />
            )}
        </Wrapper>
    );
};
