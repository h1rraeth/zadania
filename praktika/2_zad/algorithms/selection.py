def selection_sort(arr, draw_func, title="Сортировка выбором"):
    array = arr.copy()
    n = len(array)
    steps = 0
    sorted_indices = []

    for i in range(n):
        min_idx = i
        draw_func(
            array,
            comparing=[i],
            sorted_indices=sorted_indices[:],
            title=title,
            step_count=steps,
        )

        for j in range(i + 1, n):
            steps += 1
            draw_func(
                array,
                comparing=[min_idx, j],
                sorted_indices=sorted_indices[:],
                title=title,
                step_count=steps,
            )

            if array[j] < array[min_idx]:
                min_idx = j

        if min_idx != i:
            array[i], array[min_idx] = array[min_idx], array[i]
            draw_func(
                array,
                comparing=[i, min_idx],
                sorted_indices=sorted_indices[:],
                title=title,
                step_count=steps,
            )

        sorted_indices.append(i)
        draw_func(
            array,
            comparing=[],
            sorted_indices=sorted_indices[:],
            title=title,
            step_count=steps,
        )

    draw_func(
        array,
        comparing=[],
        sorted_indices=list(range(n)),
        title=title + " — Завершено!",
        step_count=steps,
    )
    return array, steps
