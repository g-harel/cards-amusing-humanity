import React, {useState, useEffect} from "react";

interface IProps {
    result: () => Promise<number>;
}

export const Counter: React.FunctionComponent<IProps> = (props) => {
    const [target, setTarget] = useState<number>(0);
    const [current, setCurrent] = useState<number>(0);
    const [result, setResult] = useState<null | number>(null);

    // Update target to a random number unless result is set.
    const updateTarget = () => {
        if (result === null) {
            setTarget(Math.floor(Math.random() * 100));
        } else if (target !== result) {
            setTarget(result);
        }
    };

    if (current === target) {
        updateTarget();
    } else {
        // Update current value to be closer to target.
        // Delay is increased as current value approaches target.
        const proximity = Math.pow(1 - Math.abs(target - current) / 100, 4);
        if (current < target) {
            setTimeout(() => setCurrent(current + 1), 200 * proximity);
        } else {
            setTimeout(() => setCurrent(current - 1), 200 * proximity);
        }
    }

    // Result is fetched and target randomized on initial render.
    useEffect(() => {
        props.result().then(setResult);
        updateTarget();
    }, []);

    return <span>{current}</span>;
};
