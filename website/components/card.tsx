import React from "react";
import styled, {css} from "styled-components";

export interface Props {
    type: "black" | "white" | "outline";
    content: string;
    onClick?: () => any;
}

interface BaseProps {
    angle?: number;
    x?: number;
    y?: number;
}

const Wrapper = styled.div`
    padding: 3rem;
`;

const Base = styled.div<BaseProps>`
    border-radius: 0.7rem;
    font-weight: 600;
    height: 18rem;
    padding: 1rem 1.5rem;
    transition: transform 0.1s ease;
    user-select: none;
    width: 13rem;

    /* TODO logo ::after */

    ${(p) => css`
        transform: rotate(${p.angle || 0}deg)
            translate(${p.x || 0}rem, ${p.y || 0}rem);
    `}
`;

// Used to style both "Black" and "White" together.
const Solid = styled(Base)<BaseProps>`
    cursor: pointer;

    &:hover {
        ${(p) => css`
            transform: rotate(
                    calc(
                        ${p.angle || 0}deg ${(p.angle || 0) < 0 ? "+" : "-"}
                            0.3deg
                    )
                )
                scale(1.008) translate(${p.x || 0}rem, ${p.y || 0}rem);
        `}
    }

    &:active {
        /* Remove hover styles. */
        ${(p) => css`
            transform: rotate(
                    calc(
                        ${p.angle || 0}deg ${(p.angle || 0) < 0 ? "+" : "-"}
                            0.3deg
                    )
                )
                translate(${p.x || 0}rem, ${p.y || 0}rem);
        `}
    }
`;

const Black = styled(Solid)`
    background-color: #000;
    color: #fff;
`;

const White = styled(Solid)`
    background-color: #fff;
    color: #000;
`;

const Shadow = styled(Base)`
    background-color: #000;
    opacity: 0.1;
`;

const Outline = styled(Base)`
    border: 0.1rem dashed #fff;
    opacity: 0.4;
`;

const Collapse = styled.div`
    height: 0;
`;

export const Card: React.StatelessComponent<Props> = (props) => {
    const angle = 10 * (Math.random() - 0.5);

    if (props.type === "outline") {
        return (
            <Wrapper>
                <Outline angle={angle} />
            </Wrapper>
        );
    }

    return (
        <Wrapper>
            <Collapse>
                <Shadow angle={angle} x={-0.8} y={0.5} />
            </Collapse>
            {props.type === "black" ? (
                <Black angle={angle} onClick={props.onClick}>
                    {props.content}
                </Black>
            ) : (
                <White angle={angle} onClick={props.onClick}>
                    {props.content}
                </White>
            )}
        </Wrapper>
    );
};
