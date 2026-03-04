"""
RAM utilization monitor with smoothing and threshold detection
Implements rolling window averaging to prevent false positives
"""
import psutil
import time
from typing import List, Tuple, Optional
from collections import deque
import logging
from dataclasses import dataclass
from datetime import datetime
import json