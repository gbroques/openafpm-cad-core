from pathlib import Path
from pprint import pprint
from typing import List, Tuple

def load_airfoil_coordinates(filepath: Path) -> List[Tuple[float, float]]:
    """Load airfoil coordinates from .dat file
    
    Coordinates follow counterclockwise convention:
    - Starts at upper surface trailing edge (x=1.0, y>0)
    - Goes to leading edge (x=0.0)
    - Continues to lower surface trailing edge (x=1.0, y<0)
    
    See: https://m-selig.ae.illinois.edu/ads/coord_seligFmt_fig/airfoilCoordinatesSm.png
    """
    coordinates = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    x, y = float(parts[0]), float(parts[1])
                    coordinates.append((x, y))
                except ValueError:
                    continue
    return coordinates

# Load airfoil coordinates
coordinates = load_airfoil_coordinates(Path(__file__).parent / 'USNPS4.dat')
pprint(coordinates)
print(f"Loaded {len(coordinates)} airfoil coordinates")
