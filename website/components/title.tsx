import React from "react";
import styled from "styled-components";

const Wrapper = styled.h1`
    margin: 0;
    padding: 2rem;
    text-shadow: 0 0 4px #121212;
    user-select: none;
`;

export const Title: React.FunctionComponent = () => (
    <Wrapper>
        Cards <br /> Amusing <br /> Humanity
    </Wrapper>
);
