import React from "react";
import styled from "styled-components";

import {Game} from "./game";

const Wrapper = styled.div`
    display: flex;
    flex-flow: wrap;
    padding: 3rem;
`;

export const Board: React.FunctionComponent = () => {
    // TODO
    const result = null;

    return (
        <Wrapper>
            {!result && (
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
