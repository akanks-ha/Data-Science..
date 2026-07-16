import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from itertools import permutations

# 3x3 grid positions (row, col) for dots 1-9
# Row 1: 1, 2, 3
# Row 2: 4, 5, 6
# Row 3: 7, 8, 9

positions = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 9: (2, 2)
}

# Android pattern lock adjacency rules
# A dot can be connected to another only if no unvisited dot lies between them
def get_between(a, b):
    """Returns the dot between a and b if they are in the same row, column, or diagonal"""
    r1, c1 = positions[a]
    r2, c2 = positions[b]
    
    dr = r2 - r1
    dc = c2 - c1
    
    # Check if there's a dot directly between them
    if dr == 0 and abs(dc) == 2:  # Same row, skip one
        return next(k for k, v in positions.items() if v == (r1, c1 + dc // 2))
    elif dc == 0 and abs(dr) == 2:  # Same column, skip one
        return next(k for k, v in positions.items() if v == (r1 + dr // 2, c1))
    elif abs(dr) == 2 and abs(dc) == 2:  # Diagonal, skip one
        return next(k for k, v in positions.items() if v == (r1 + dr // 2, c1 + dc // 2))
    return None

def is_valid_move(a, b, visited):
    """Check if moving from a to b is valid given visited dots"""
    between = get_between(a, b)
    if between is not None and between not in visited:
        return False
    return True

def is_valid_pattern(path):
    """Check if entire pattern is valid"""
    visited = set()
    for i in range(len(path) - 1):
        visited.add(path[i])
        if not is_valid_move(path[i], path[i+1], visited):
            return False
    return True

def pattern_to_binary(path, total_dots=9):
    """Convert pattern to binary representation (which dots are used and in order)"""
    binary = ['0'] * total_dots
    for i, dot in enumerate(path):
        binary[dot - 1] = '1'
    return ''.join(binary)

def is_m_shape(path):
    """
    Check if a pattern forms an M shape using first two rows (dots 1-6)
    M shape: starts bottom-left, goes up, diagonal down to center, diagonal up, then down to bottom-right
    Valid M patterns use dots from rows 1 and 2 only (dots 1-6)
    
    Classic M shape connections:
    - Left vertical: 4->1 or 1->4
    - Left diagonal: 1->5 or 5->1  
    - Right diagonal: 5->3 or 3->5
    - Right vertical: 3->6 or 6->3
    
    Two possible M orientations:
    M1: 4-1-5-3-6 (bottom-left up, diagonal to center-bottom, up to top-right, down)
    M2: 4-1-2-3-6 (using top row as the peaks)
    """
    # Only use dots from rows 1 and 2 (dots 1-6)
    if not all(d in [1, 2, 3, 4, 5, 6] for d in path):
        return False
    
    # M shape must use exactly these key dots
    path_set = set(path)
    
    # Define valid M patterns
    # M shape requires: two vertical sides and a middle valley
    # Pattern 1: 4-1-5-3-6 (classic M with center valley at dot 5)
    m_pattern1 = [4, 1, 5, 3, 6]
    # Pattern 2: 6-3-5-1-4 (reverse of pattern 1)
    m_pattern2 = [6, 3, 5, 1, 4]
    # Pattern 3: 4-1-2-3-6 (M using top row)
    m_pattern3 = [4, 1, 2, 3, 6]
    # Pattern 4: 6-3-2-1-4 (reverse of pattern 3)
    m_pattern4 = [6, 3, 2, 1, 4]
    
    valid_m_patterns = [m_pattern1, m_pattern2, m_pattern3, m_pattern4]
    
    # Check if path matches any valid M pattern (considering subsequences)
    for m in valid_m_patterns:
        if list(path) == m:
            return True
    
    return False

def find_all_m_patterns():
    """Find all valid M-shaped patterns"""
    # Generate permutations of dots in first two rows
    first_two_rows = [1, 2, 3, 4, 5, 6]
    
    m_patterns = []
    
    # Check patterns of length 4-6
    for length in range(4, 7):
        for perm in permutations(first_two_rows, length):
            if is_m_shape(perm) and is_valid_pattern(perm):
                m_patterns.append(list(perm))
    
    # Remove duplicates
    unique_patterns = []
    seen = set()
    for p in m_patterns:
        key = tuple(p)
        if key not in seen:
            seen.add(key)
            unique_patterns.append(p)
    
    return unique_patterns

def visualize_pattern(path, pattern_num, binary_code):
    """Visualize a single M pattern on the grid"""
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    
    # Draw grid dots
    dot_colors = {dot: 'lightblue' for dot in range(1, 10)}
    for dot in path:
        dot_colors[dot] = 'orange'
    
    # Draw connections
    for i in range(len(path) - 1):
        r1, c1 = positions[path[i]]
        r2, c2 = positions[path[i+1]]
        ax.plot([c1, c2], [-r1, -r2], 'r-', linewidth=3, zorder=1)
        
        # Add arrow to show direction
        mid_x = (c1 + c2) / 2
        mid_y = (-r1 + -r2) / 2
        dx = (c2 - c1) * 0.1
        dy = (-r2 - -r1) * 0.1
        ax.annotate('', xy=(mid_x + dx, mid_y + dy), xytext=(mid_x - dx, mid_y - dy),
                   arrowprops=dict(arrowstyle='->', color='darkred', lw=2))
    
    # Draw dots
    for dot, (r, c) in positions.items():
        circle = plt.Circle((c, -r), 0.2, color=dot_colors[dot], zorder=2, ec='black', lw=1.5)
        ax.add_patch(circle)
        ax.text(c, -r, str(dot), ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)
    
    # Add order numbers
    for i, dot in enumerate(path):
        r, c = positions[dot]
        ax.text(c + 0.25, -r + 0.25, str(i+1), ha='center', va='center', 
               fontsize=8, color='blue', fontweight='bold')
    
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-2.5, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'M-Pattern #{pattern_num}\nPath: {" → ".join(map(str, path))}\nBinary: {binary_code}', 
                fontsize=11, fontweight='bold')
    
    # Add legend
    legend_elements = [
        mpatches.Patch(color='orange', label='Used dots'),
        mpatches.Patch(color='lightblue', label='Unused dots'),
        plt.Line2D([0], [0], color='red', linewidth=2, label='Pattern path')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8)
    
    plt.tight_layout()
    return fig

def main():
    print("Finding all valid M-shaped patterns in first two rows...")
    print("="*60)
    
    m_patterns = find_all_m_patterns()
    
    if not m_patterns:
        print("No M-shaped patterns found!")
        return
    
    print(f"Found {len(m_patterns)} M-shaped pattern(s):\n")
    
    figs = []
    for i, pattern in enumerate(m_patterns):
        binary = pattern_to_binary(pattern)
        print(f"Pattern #{i+1}:")
        print(f"  Path: {' → '.join(map(str, pattern))}")
        print(f"  Binary (dots 1-9 used): {binary}")
        print(f"  Dots used: {sorted(set(pattern))}")
        print()
        
        fig = visualize_pattern(pattern, i+1, binary)
        figs.append(fig)
    
    # Show all patterns in a grid layout
    n_patterns = len(m_patterns)
    cols = min(3, n_patterns)
    rows = (n_patterns + cols - 1) // cols
    
    fig_all, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    if n_patterns == 1:
        axes = [axes]
    elif rows == 1:
        axes = list(axes)
    else:
        axes = [ax for row in axes for ax in row]
    
    for i, (pattern, ax) in enumerate(zip(m_patterns, axes)):
        binary = pattern_to_binary(pattern)
        
        dot_colors = {dot: 'lightblue' for dot in range(1, 10)}
        for dot in pattern:
            dot_colors[dot] = 'orange'
        
        for j in range(len(pattern) - 1):
            r1, c1 = positions[pattern[j]]
            r2, c2 = positions[pattern[j+1]]
            ax.plot([c1, c2], [-r1, -r2], 'r-', linewidth=3, zorder=1)
        
        for dot, (r, c) in positions.items():
            circle = plt.Circle((c, -r), 0.2, color=dot_colors[dot], zorder=2, ec='black', lw=1.5)
            ax.add_patch(circle)
            ax.text(c, -r, str(dot), ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)
        
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-2.5, 0.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'M-Pattern #{i+1}\n{" → ".join(map(str, pattern))}\nBinary: {binary}', fontsize=10)
    
    # Hide empty subplots
    for i in range(n_patterns, len(axes)):
        axes[i].set_visible(False)
    
    plt.suptitle('All Valid M-Shaped Lock Patterns\n(First Two Rows)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('m_patterns_all.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"\nVisualization saved as 'm_patterns_all.png'")

if __name__ == "__main__":
    main()