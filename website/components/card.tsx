import React from "react";
import styled from "styled-components";

export interface Props {
    type: "black" | "white" | "outline";
    content: string;
}

const Wrapper = styled.div`
    padding: 3rem;
`;

const Base = styled.div`
    border-radius: 0.7rem;
    font-weight: 600;
    height: 18rem;
    padding: 1rem 1.5rem;
    width: 13rem;
`;

const Collapse = styled.div`
    height: 0;
`;

export const Card: React.StatelessComponent<Props> = (props) => {
    const angle = 10 * (Math.random() - 0.5);

    if (props.type === "outline") {
        return (
            <Wrapper>
                <Base
                    style={{
                        border: "0.1rem dashed #fff",
                        opacity: 0.4,
                        transform: `rotate(${angle}deg)`,
                    }}
                />
            </Wrapper>
        );
    }

    return (
        <Wrapper>
            <Collapse>
                <Base
                    style={{
                        backgroundColor: "#000",
                        opacity: 0.1,
                        transform: `rotate(${angle}deg) translate(-0.8rem, 0.5rem)`,
                    }}
                />
            </Collapse>
            <Base
                style={{
                    backgroundColor: props.type === "black" ? "#000" : "#fff",
                    color: props.type === "black" ? "#fff" : "#000",
                    transform: `rotate(${angle}deg)`,
                }}
            >
                {props.content}
                {/* TODO logo */}
            </Base>
        </Wrapper>
    );
};
