INSERT INTO lookup (
    id,
    group_code,
    group_desc,
    value,
    label,
    order_index,
    is_hidden,
    modified_date
) VALUES
('empstat01', 'EMP_STATUS', 'Employee Status', 'ACTIVE', 'Active', 1, FALSE, NOW()),
('empstat02', 'EMP_STATUS', 'Employee Status', 'INACTIVE', 'Inactive', 2, FALSE, NOW()),
('empstat03', 'EMP_STATUS', 'Employee Status', 'RESIGNED', 'Resigned', 3, FALSE, NOW()),
('empstat04', 'EMP_STATUS', 'Employee Status', 'TERMINATED', 'Terminated', 4, FALSE, NOW())
('uomtype01', 'UOM_TYPE', 'Unit of Measure Type', 'QUANTITY', 'Quantity', 1, FALSE, NOW()),
('uomtype02', 'UOM_TYPE', 'Unit of Measure Type', 'WEIGHT', 'Weight', 2, FALSE, NOW()),
('uomtype03', 'UOM_TYPE', 'Unit of Measure Type', 'VOLUME', 'Volume', 3, FALSE, NOW()),
('uomtype04', 'UOM_TYPE', 'Unit of Measure Type', 'LENGTH', 'Length', 4, FALSE, NOW()),
('uomtype05', 'UOM_TYPE', 'Unit of Measure Type', 'AREA', 'Area', 5, FALSE, NOW()),
('uomtype06', 'UOM_TYPE', 'Unit of Measure Type', 'TIME', 'Time', 6, FALSE, NOW()),
('itemcat01', 'ITEM_CATEGORY', 'Item Category', 'RAW_MATERIAL', 'Raw Material', 1, FALSE, NOW()),
('itemcat02', 'ITEM_CATEGORY', 'Item Category', 'FINISHED_GOOD', 'Finished Good', 2, FALSE, NOW()),
('itemcat03', 'ITEM_CATEGORY', 'Item Category', 'SEMI_FINISHED', 'Semi Finished', 3, FALSE, NOW()),
('itemcat04', 'ITEM_CATEGORY', 'Item Category', 'CONSUMABLE', 'Consumable', 4, FALSE, NOW()),
('itemcat05', 'ITEM_CATEGORY', 'Item Category', 'SPARE_PART', 'Spare Part', 5, FALSE, NOW()),
('itemcat06', 'ITEM_CATEGORY', 'Item Category', 'SERVICE', 'Service', 6, FALSE, NOW()),
('itemcat07', 'ITEM_CATEGORY', 'Item Category', 'FIXED_ASSET', 'Fixed Asset', 7, FALSE, NOW()),
('stmv01', 'STOCK_MVMNT', 'Stock Movement Type', 'adj', 'Adjustment', 1, FALSE, NOW()),
('stmv02', 'STOCK_MVMNT', 'Stock Movement Type', 'trf', 'Transfer', 2, FALSE, NOW());