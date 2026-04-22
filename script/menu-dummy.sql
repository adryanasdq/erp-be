INSERT INTO admin.menu (
    id,
    title,
    url,
    icon,
    parent_id,
    order_index,
    is_hidden,
    modified_date
) VALUES
-- root
('a1b2c3d4e5', 'Home', '/', '', NULL, 1, FALSE, NOW()),

-- admin
('f6g7h8i9j0', 'Admin', '/admin', '', NULL, 2, FALSE, NOW()),
('k1l2m3n4o5', 'Menu Mgmt', '/admin/tools/menu-mgmt', 'layout-dashboard.svg', 'f6g7h8i9j0', 1, FALSE, NOW()),
('p6q7r8s9t0', 'Lookup', '/admin/tools/lookup', 'file-search-corner.svg', 'f6g7h8i9j0', 2, FALSE, NOW()),

-- human resource
('u1v2w3x4y5', 'Human Resource', '/human-resource', '', NULL, 3, FALSE, NOW()),
('z6a7b8c9d0', 'Department', '/human-resource/department', 'building.svg', 'u1v2w3x4y5', 1, FALSE, NOW()),
('e1f2g3h4i5', 'Employee', '/human-resource/employee', 'user.svg', 'u1v2w3x4y5', 2, FALSE, NOW()),
('j6k7l8m9n0', 'Position', '/human-resource/position', 'briefcase.svg', 'u1v2w3x4y5', 3, FALSE, NOW()),

-- inventory
('inv123abcd', 'Inventory', '/inventory', '', NULL, 4, FALSE, NOW()),
('o1p2q3r4s5', 'Warehouse', '/inventory/warehouse', 'warehouse.svg', 'inv123abcd', 1, FALSE, NOW()),
('t6u7v8w9x0', 'Uom', '/inventory/uom', 'ruler.svg', 'inv123abcd', 2, FALSE, NOW()),
('y1z2a3b4c5', 'Item', '/inventory/item', 'package.svg', 'inv123abcd', 3, FALSE, NOW()),
('d6e7f8g9h0', 'Stock Balance', '/inventory/stock-balance', 'chart-bar.svg', 'inv123abcd', 4, FALSE, NOW()),
('i1j2k3l4m5', 'Uom Conversion', '/inventory/uom-conversion', 'exchange.svg', 'inv123abcd', 5, FALSE, NOW()),
('n6o7p8q9r0', 'Stock Movement', '/inventory/stock-movement', 'arrows-right-left.svg', 'inv123abcd', 6, FALSE, NOW()),

-- purchasing
('purc000001', 'Purchasing', '/purchasing', '', NULL, 6, FALSE, NOW()),
('purc000002', 'Purchase Order', '/purchasing/purchase-order', '', 'purc000001', 1, FALSE, NOW()),
('purc000003', 'Good Receipt', '/purchasing/good-receipt', '', 'purc000001', 2, FALSE, NOW()),

-- sales
('sales00001', 'Sales', '/sales', '', NULL, 7, FALSE, NOW()),
('sales00002', 'Customer', '/sales/customer', '', 'sales00001', 1, FALSE, NOW()),
('sales00003', 'Delivery', '/sales/delivery', '', 'sales00001', 2, FALSE, NOW()),
('sales00004', 'Sales Order', '/sales/sales-order', '', 'sales00001', 3, FALSE, NOW()),

-- accounting
('acct000001', 'Accounting', '/accounting', '', NULL, 8, FALSE, NOW()),
('acct000002', 'Account', '/accounting/account', '', 'acct000001', 1, FALSE, NOW()),
('acct000003', 'Journal', '/accounting/journal', '', 'acct000001', 2, FALSE, NOW());

-- wildcard
('s1t2u3v4w5', 'Not Found', '*', '', NULL, 5, FALSE, NOW());