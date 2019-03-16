import React from "react";
import styled from "styled-components";

const Wrapper = styled.h1`
    height: 0;
    margin: 0;
    text-shadow: 0 0 4px #121212;
    transform: translate(3rem, 3rem);
    user-select: none;
    width: 0;
`;

export const Title: React.FunctionComponent = () => (
    <Wrapper>
        Cards <br /> Amusing <br /> Humanity
    </Wrapper>
);
