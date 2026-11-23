import { useCallback, useState } from "react"

export class Cell {
    color: string

    constructor(color: string = "#334155") {
        this.color = color
    }
}

export interface Grid {
    cells: Cell[][]
    gridLength: number
    gridWidth: number
    cellLength: number
    cellWidth: number
}

export function createGrid(
    gridLength: number,
    gridWidth: number,
    cellLength: number,
    cellWidth: number
): Grid {
    const cells: Cell[][] = []
    for (let row = 0; row < gridWidth; row++) {
        const cellsInRow: Cell[] = []
        for (let col = 0; col < gridLength; col++) {
            cellsInRow.push(new Cell())
        }
        cells.push(cellsInRow)
    }
    return { cells, gridLength, gridWidth, cellLength, cellWidth }
}

export function updateCellColor(
    grid: Grid,
    row: number,
    col: number,
    color: string
): Grid {
    return {
        ...grid,
        cells: grid.cells.map((cellsInRow, r) =>
            r === row
                ? cellsInRow.map((cell, c) => (c === col ? new Cell(color) : cell))
                : cellsInRow
        )
    }
}

export function drawGrid(ctx: CanvasRenderingContext2D, grid: Grid): void {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
    for (let row = 0; row < grid.gridWidth; row++) {
        for (let col = 0; col < grid.gridLength; col++) {
            const cell = grid.cells[row]?.[col]
            if (!cell) continue
            ctx.fillStyle = cell.color
            ctx.fillRect(
                col * grid.cellLength,
                row * grid.cellWidth,
                grid.cellLength,
                grid.cellWidth
            )
        }
    }
}

export function mouseToCell(
    grid: Grid,
    canvas: HTMLCanvasElement,
    clientX: number,
    clientY: number
): { row: number; col: number } | null {
    const rect = canvas.getBoundingClientRect()
    const col = Math.floor((clientX - rect.left) / grid.cellLength)
    const row = Math.floor((clientY - rect.top) / grid.cellWidth)
    if (
        col < 0 || col >= grid.gridLength ||
        row < 0 || row >= grid.gridWidth ||
        Number.isNaN(col) || Number.isNaN(row)
    ) {
        return null
    }
    return { row, col }
}

export function useGrid(
    gridLength: number,
    gridWidth: number,
    cellLength: number,
    cellWidth: number
) {
    const [grid, setGrid] = useState<Grid>(() =>
        createGrid(gridLength, gridWidth, cellLength, cellWidth)
    )

    const setCellColor = useCallback(
        (row: number, col: number, color: string) => {
            setGrid((prev) => updateCellColor(prev, row, col, color))
        },
        []
    )

    return { grid, setCellColor }
}
