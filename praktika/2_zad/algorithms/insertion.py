def insertion_sort(arr, draw_func, title="Сортировка вставками"):
    array = arr.copy()
    n = len(array)
    steps = 0
    sorted_indices = [0]

    for i in range(1, n):
        key = array[i]
        j = i - 1

        draw_func(
            array,
            comparing=[i],
            sorted_indices=sorted_indices[:],
            title=title,
            step_count=steps,
        )

        while j >= 0 and array[j] > key:
            steps += 1
            array[j + 1] = array[j]
            draw_func(
                array,
                comparing=[j, i],
                sorted_indices=sorted_indices[:],
                title=title,
                step_count=steps,
            )
            j -= 1

        array[j + 1] = key
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
