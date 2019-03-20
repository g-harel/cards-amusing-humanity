import React from "react";
import styled, {keyframes, css} from "styled-components";

interface Props {
    color?: string;
    loading?: true;
    scale?: number;
}

const Wrapper = styled.div<Props>`
    height: 0;
    ${(p) => css`
        color: ${p.color || "white"};
        transform: scale(${p.scale || 1}) translateY(-150px);
    `}
`;

const Base = styled.div`
    border-radius: 30px;
    box-sizing: border-box;
    height: 300px;
    width: 200px;
`;

const slideFull = keyframes`
    0% {transform: rotate(20deg) translateX(80px)}
    20% {transform: rotate(-20deg) translateX(-80px)}
    50% {transform: rotate(20deg) translateX(80px)}
    100% {transform: rotate(20deg) translateX(80px)}
`;

const Full = styled(Base)<Props>`
    animation: 2s ${slideFull} ease infinite;
    background-color: currentColor;
    ${(p) =>
        !p.loading &&
        css`
            animation-play-state: paused;
        `}
`;

const slideOutline = keyframes`
    0% {transform: rotate(-20deg) translateX(-80px)}
    20% {transform: rotate(20deg) translateX(80px)}
    50% {transform: rotate(-20deg) translateX(-80px)}
    100% {transform: rotate(-20deg) translateX(-80px)}
`;

const Outline = styled(Base)<Props>`
    animation: 2s ${slideOutline} ease infinite;
    border: 18px solid currentColor;
    ${(p) =>
        !p.loading &&
        css`
            animation-play-state: paused;
        `}
`;

const Collapse = styled.div`
    height: 0;
`;

export const Logo: React.FunctionComponent<Props> = (props) => (
    <Wrapper {...props}>
        <Collapse>
            <Full {...props} />
        </Collapse>
        <Outline {...props} />
    </Wrapper>
);
