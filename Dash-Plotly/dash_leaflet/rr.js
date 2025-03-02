function approximateRoot(func, initialGuess, tolerance = 1e-7, maxIterations = 1000) {
    let x = initialGuess;
    for (let i = 0; i < maxIterations; i++) {
        const fx = func(x);
        const dfx = (func(x + tolerance) - fx) / tolerance; // Numerical derivative
        const xNew = x - fx / dfx;
        if (Math.abs(xNew - x) < tolerance) {
            return xNew;
        }
        x = xNew;
    }
    throw new Error('Maximum iterations exceeded');
}