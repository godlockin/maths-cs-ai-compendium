-- wide-tables.lua
-- Mark wide tables so the PDF CSS can place them on a landscape named page.
--
-- Heuristic: a table is "wide" when it has >= 6 columns, or >= 5 columns AND
-- it contains an inline Image (formula PNGs need extra width). pandoc attaches
-- the class to the HTML <table>; the CSS rule `table.wide { page: wide }`
-- maps it to `@page wide { size: A4 landscape }`.
--
-- Uses pandoc.walk_block so it works across pandoc versions without touching
-- the Table/Cell AST shape directly.

local function contains_image(tbl)
  local found = false
  local filters = {
    Image = function() found = true end,
  }
  pandoc.walk_block(tbl, filters)
  return found
end

function Table(tbl)
  local ncols = tbl.colspecs and #tbl.colspecs or 0
  local wide = ncols >= 6 or (ncols >= 5 and contains_image(tbl))
  if wide then
    tbl.classes = tbl.classes or pandoc.List({})
    tbl.classes:insert('wide')
  end
  return tbl
end