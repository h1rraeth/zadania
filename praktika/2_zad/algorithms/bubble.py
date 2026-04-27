def bubble_sort(arr, draw_func, title="Сортировка пузырьком"):
    array = arr.copy()
    n = len(array)
    steps = 0
    sorted_indices = []

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            steps += 1
            draw_func(
                array,
                comparing=[j, j + 1],
                sorted_indices=sorted_indices[:],
                title=title,
                step_count=steps,
            )

            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
                draw_func(
                    array,
                    comparing=[j, j + 1],
                    sorted_indices=sorted_indices[:],
                    title=title,
                    step_count=steps,
                )

        sorted_indices.append(n - i - 1)
        draw_func(
            array,
            comparing=[],
            sorted_indices=sorted_indices[:],
            title=title,
            step_count=steps,
        )

        if not swapped:
            break

    draw_func(
        array,
        comparing=[],
        sorted_indices=list(range(n)),
        title=title + " — Завершено!",
        step_count=steps,
    )
    return array, steps
