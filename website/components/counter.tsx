import React, {useState} from "react";

interface IProps {
    target: number;
    callback?: () => any;
}

export const Counter: React.FunctionComponent<IProps> = (props) => {
    const [current, setCurrent] = useState<number>(0);

    if (props.target !== current) {
        // Update current value to be closer to target.
        // Delay is increased as current value approaches target.
        const proximity = Math.pow(
            1 - Math.abs(props.target - current) / 100,
            4,
        );
        setTimeout(() => setCurrent(current + 1), 200 * proximity);
    } else {
        if (props.callback) {
            props.callback();
        }
    }

    return <span>{current}</span>;
};
