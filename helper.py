import pygame


__all__ = ('gravity', 'cof', 'event_mappings', 'rotate_along_pivot')


gravity = -1  # default constant for gravity
cof = 0.9  # default constant for the coefficient of friction

event_mappings = {}  # handle custom events


def rotate_along_pivot(sprite, pos, pivot, angle):
    # offset from pivot to center
    image_rect = sprite.original_surface.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # rotated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # rotated image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(sprite.original_surface, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    return rotated_image_rect, rotated_image
